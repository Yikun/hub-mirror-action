import argparse
import logging
from typing import Dict, List, Optional, Union

import git

logger = logging.getLogger(__name__)


class Progress(git.remote.RemoteProgress):
    def __init__(self, name: str) -> None:
        super(Progress, self).__init__()
        self.name: str = name

    def update(
        self,
        op_code: int,
        cur_count: int,
        max_count: Optional[int] = None,
        message: str = "",
    ) -> None:
        logger.debug(f"Process {self.name}, {self._cur_line}")


def str2bool(v: Union[str, bool]) -> bool:
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    if v.lower() in ("no", "false", "f", "n", "0"):
        return False
    raise argparse.ArgumentTypeError("Boolean value expected.")


def cov2sec(s: str) -> int:
    _h = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
    if _h.get(s[-1]):
        return int(s[:-1]) * _h.get(s[-1], 1)
    return int(s)


def str2list(s: Optional[str]) -> List[str]:
    # Change "a, b" to ['a', 'b']
    if not s:
        return []
    return s.replace(" ", "").split(",")


# "a=>b, c=>d" to {'a': 'b', 'c': 'd'}
def str2map(s: Optional[str]) -> Dict[str, str]:
    if not s:
        return {}
    mappings: Dict[str, str] = {}
    mappings_list = str2list(s)
    for maping in mappings_list:
        old, new = maping.split("=>")
        mappings[old] = new
    return mappings
