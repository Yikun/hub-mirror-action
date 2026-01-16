import functools
import logging
import time
from typing import Any, Dict, List

import requests

from platforms import GitPlatform, get_platform

logger = logging.getLogger(__name__)


class Hub(object):
    def __init__(
        self,
        src: str,
        dst: str,
        dst_token: str,
        account_type: str = "user",
        clone_style: str = "https",
        src_account_type: str = "",
        dst_account_type: str = "",
        src_endpoint: str = "",
        dst_endpoint: str = "",
        api_timeout: int = 60,
    ) -> None:
        self.api_timeout: int = api_timeout
        self.account_type: str = account_type
        self.src_account_type: str = src_account_type or account_type
        self.dst_account_type: str = dst_account_type or account_type
        self.src_type: str
        self.src_account: str
        self.dst_type: str
        self.dst_account: str
        self.src_type, self.src_account = src.split("/")
        self.dst_type, self.dst_account = dst.split("/")
        self.src_platform: GitPlatform = get_platform(
            self.src_type, endpoint=src_endpoint
        )
        self.dst_platform: GitPlatform = get_platform(
            self.dst_type, endpoint=dst_endpoint
        )
        self.src_platform.validate_account_type(
            self.src_account_type, "source"
        )
        self.dst_platform.validate_account_type(
            self.dst_account_type, "destination"
        )
        self.dst_token: str = dst_token
        self.session: requests.Session = requests.Session()
        self.src_repo_base: str = self.src_platform.get_clone_repo_base(
            self.src_account, clone_style
        )
        self.dst_repo_base: str = self.dst_platform.get_push_repo_base(
            self.dst_account
        )

    def has_dst_repo(self, repo_name: str) -> bool:
        url: str = self.dst_platform.repo_list_url(
            self.dst_account, self.dst_account_type
        )
        repo_names: List[str] = self._get_all_repo_names(url)
        if not repo_names:
            logger.warning("Destination repos is [].")
            return False
        return repo_name in repo_names

    def create_dst_repo(self, repo_name: str) -> bool:
        created: bool = False
        if not self.has_dst_repo(repo_name):
            logger.info(f"{repo_name} doesn't exist, create it...")
            created = self.dst_platform.create_repo(
                self.session,
                self.dst_account,
                self.dst_account_type,
                repo_name,
                self.dst_token,
                self.api_timeout,
            )
        else:
            logger.info(f"{repo_name} repo exist, skip creating...")
        if created:
            time.sleep(2)
        return created

    def dynamic_list(self) -> List[str]:
        url: str = self.src_platform.repo_list_url(
            self.src_account, self.src_account_type
        )
        return self._get_all_repo_names(url)

    @functools.lru_cache
    def _get_all_repo_names(self, url: str, page: int = 1) -> List[str]:
        per_page: int = 60
        api: str = url + f"?page={page}&per_page=" + str(per_page)
        # TODO: src_token support
        response: requests.Response = self.session.get(
            api, timeout=self.api_timeout
        )
        all_items: List[str] = []
        if response.status_code != 200:
            logger.error(f"Repo getting failed: {response.text}")
            return all_items
        items: List[Dict[str, Any]] = response.json()
        if items:
            names: List[str] = [i["name"] for i in items]
            return names + self._get_all_repo_names(url, page=page + 1)
        return all_items
