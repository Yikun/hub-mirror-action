import logging
import sys
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

import click

from hub import Hub
from mirror import Mirror
from utils import str2list, str2map

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class MirrorConfig:
    src: str
    dst: str
    dst_token: str
    account_type: str = "user"
    src_account_type: str = ""
    dst_account_type: str = ""
    src_endpoint: str = ""
    dst_endpoint: str = ""
    clone_style: str = "https"
    cache_path: str = "hub-mirror-cache"
    black_list: str = ""
    white_list: str = ""
    static_list: str = ""
    force_update: bool = False
    debug: str = "INFO"
    timeout: str = "30m"
    api_timeout: int = 60
    mappings: str = ""
    lfs: bool = False


class HubMirror(object):
    def __init__(self, config: MirrorConfig) -> None:
        self.config: MirrorConfig = config
        self.white_list: List[str] = str2list(config.white_list)
        self.black_list: List[str] = str2list(config.black_list)
        self.static_list: List[str] = str2list(config.static_list)
        self.mappings: Dict[str, str] = str2map(config.mappings)

    def test_black_white_list(self, repo: str) -> bool:
        if repo in self.black_list:
            logger.info(f"Skip, {repo} in black list: {self.black_list}")
            return False

        if self.white_list and repo not in self.white_list:
            logger.info(
                f"Skip, {repo} not in white list: {self.white_list}"
            )
            return False

        return True

    def run(self) -> None:
        config = self.config
        hub = Hub(
            config.src,
            config.dst,
            config.dst_token,
            account_type=config.account_type,
            clone_style=config.clone_style,
            src_account_type=config.src_account_type,
            dst_account_type=config.dst_account_type,
            src_endpoint=config.src_endpoint,
            dst_endpoint=config.dst_endpoint,
            api_timeout=config.api_timeout,
        )

        # Using static list when static_list is set
        repos: List[str] = self.static_list
        src_repos: List[str] = repos if repos else hub.dynamic_list()

        total: int = len(src_repos)
        success: int = 0
        skip: int = 0
        failed_list: List[str] = []
        for src_repo in src_repos:
            # Set dst_repo to src_repo mapping or src_repo directly
            dst_repo: str = self.mappings.get(src_repo, src_repo)
            logger.info(f"Map {src_repo} to {dst_repo}")
            if self.test_black_white_list(src_repo):
                logger.info(f"Backup {src_repo}")
                try:
                    mirror = Mirror(
                        hub,
                        src_repo,
                        dst_repo,
                        cache=config.cache_path,
                        timeout=config.timeout,
                        force_update=config.force_update,
                        lfs=config.lfs,
                    )
                    mirror.download()
                    mirror.create()
                    mirror.push()
                    success += 1
                except Exception as e:
                    logger.error(f"Mirror failed for {src_repo}: {e}")
                    logger.debug("Mirror failure details", exc_info=True)
                    failed_list.append(src_repo)
            else:
                skip += 1
        failed: int = total - success - skip
        logger.info(
            f"Total: {total}, skip: {skip}, successed: {success}, "
            f"failed: {failed}."
        )
        logger.info(f"Failed: {failed_list}")
        if failed_list:
            sys.exit(1)


def add_options(
    options: List[Callable[[Callable[..., None]], Callable[..., None]]]
) -> Callable[[Callable[..., None]], Callable[..., None]]:
    def decorator(func: Callable[..., None]) -> Callable[..., None]:
        for option in reversed(options):
            func = option(func)
        return func

    return decorator


CLI_OPTIONS = [
    click.option("--src", required=True, help="Source name."),
    click.option("--dst", required=True, help="Destination name."),
    click.option("--dst-token", required=True, help="Token for destination hub."),
    click.option("--account-type", default="user", show_default=True),
    click.option("--src-account-type", default="", show_default=True),
    click.option("--dst-account-type", default="", show_default=True),
    click.option("--src-endpoint", default="", show_default=True),
    click.option("--dst-endpoint", default="", show_default=True),
    click.option("--clone-style", default="https", show_default=True),
    click.option("--cache-path", default="hub-mirror-cache", show_default=True),
    click.option("--black-list", default="", show_default=True),
    click.option("--white-list", default="", show_default=True),
    click.option("--static-list", default="", show_default=True),
    click.option("--force-update", default=False, type=bool, show_default=True),
    click.option(
        "--debug",
        default="INFO",
        type=str,
        show_default=True,
        help="Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).",
    ),
    click.option("--timeout", default="30m", show_default=True),
    click.option("--api-timeout", default=60, type=int, show_default=True),
    click.option("--mappings", default="", show_default=True),
    click.option("--lfs", default=False, type=bool, show_default=True),
]


def parse_log_level(value: Optional[Any]) -> int:
    if value is None:
        return logging.INFO
    if isinstance(value, bool):
        return logging.DEBUG if value else logging.INFO
    text = str(value).strip()
    if not text:
        return logging.INFO
    lowered = text.lower()
    if lowered in ("1", "true", "yes", "y", "on"):
        return logging.DEBUG
    if lowered in ("0", "false", "no", "n", "off"):
        return logging.INFO
    if lowered.isdigit():
        return int(lowered)
    name = text.upper()
    if name == "WARN":
        name = "WARNING"
    if name == "FATAL":
        name = "CRITICAL"
    level = getattr(logging, name, None)
    if isinstance(level, int):
        return level
    raise ValueError(f"Invalid log level: {value}")


@click.command()
@add_options(CLI_OPTIONS)
def main(**params: Any) -> None:
    try:
        log_level = parse_log_level(params.get("debug"))
    except ValueError as exc:
        raise click.BadParameter(str(exc))
    logging.basicConfig(
        level=log_level,
        format="{levelname}:{name}:{message}",
        style="{",
    )
    params["debug"] = logging.getLevelName(log_level)
    config = MirrorConfig(**params)
    mirror = HubMirror(config)
    mirror.run()


if __name__ == "__main__":
    main()
