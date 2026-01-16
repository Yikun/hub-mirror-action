import json
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Sequence, Type

import requests

logger = logging.getLogger(__name__)


class GitPlatform(ABC):
    name: str
    host: str
    api_base: str
    repo_field: str

    def get_clone_repo_base(self, account: str, clone_style: str) -> str:
        prefix = "https://" if clone_style == "https" else "git@"
        suffix = "/" if clone_style == "https" else ":"
        return f"{prefix}{self.host}{suffix}{account}"

    def get_push_repo_base(self, account: str) -> str:
        return f"git@{self.host}:{account}"

    def repo_list_url(self, account: str, account_type: str) -> str:
        return f"{self.api_base}/{account_type}s/{account}/{self.repo_field}"

    def _validate_account_type(
        self,
        account_type: str,
        role: str,
        allowed: Sequence[str],
    ) -> None:
        if account_type not in allowed:
            allowed_list = "', '".join(allowed)
            raise ValueError(
                f"For {self.name}, {role} account_type must be "
                f"one of '{allowed_list}'."
            )

    @abstractmethod
    def validate_account_type(self, account_type: str, role: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def create_repo(
        self,
        session: requests.Session,
        account: str,
        account_type: str,
        repo_name: str,
        token: str,
        api_timeout: int,
    ) -> bool:
        raise NotImplementedError


class GitHubPlatform(GitPlatform):
    name = "github"
    repo_field = "repos"

    def __init__(self, endpoint: str = "") -> None:
        self.host: str = "github.com"
        self.api_base: str = "https://api.github.com"

    def validate_account_type(self, account_type: str, role: str) -> None:
        self._validate_account_type(account_type, role, ("user", "org"))

    def create_repo(
        self,
        session: requests.Session,
        account: str,
        account_type: str,
        repo_name: str,
        token: str,
        api_timeout: int,
    ) -> bool:
        suffix: str = "user/repos"
        if account_type == "org":
            suffix = f"orgs/{account}/repos"
        url: str = f"{self.api_base}/{suffix}"
        data: str = json.dumps({"name": repo_name})
        response: requests.Response = session.post(
            url,
            data=data,
            headers={"Authorization": "token " + token},
            timeout=api_timeout,
        )
        if response.status_code == 201:
            logger.info("Destination repo creating accepted.")
            return True
        logger.error(f"Destination repo creating failed: {response.text}")
        return False


class GiteePlatform(GitPlatform):
    name = "gitee"
    repo_field = "repos"

    def __init__(self, endpoint: str = "") -> None:
        self.host: str = "gitee.com"
        self.api_base: str = "https://gitee.com/api/v5"

    def validate_account_type(self, account_type: str, role: str) -> None:
        self._validate_account_type(account_type, role, ("user", "org"))

    def create_repo(
        self,
        session: requests.Session,
        account: str,
        account_type: str,
        repo_name: str,
        token: str,
        api_timeout: int,
    ) -> bool:
        suffix: str = "user/repos"
        if account_type == "org":
            suffix = f"orgs/{account}/repos"
        url: str = f"{self.api_base}/{suffix}"
        response: requests.Response = session.post(
            url,
            headers={"Content-Type": "application/json;charset=UTF-8"},
            params={"name": repo_name, "access_token": token},
            timeout=api_timeout,
        )
        if response.status_code == 201:
            logger.info("Destination repo creating accepted.")
            return True
        logger.error(f"Destination repo creating failed: {response.text}")
        return False


class GitcodePlatform(GitPlatform):
    name = "gitcode"
    repo_field = "repos"

    def __init__(self, endpoint: str = "") -> None:
        self.host: str = "gitcode.com"
        self.api_base: str = "https://api.gitcode.com/api/v5"

    def validate_account_type(self, account_type: str, role: str) -> None:
        self._validate_account_type(account_type, role, ("user", "org"))

    def create_repo(
        self,
        session: requests.Session,
        account: str,
        account_type: str,
        repo_name: str,
        token: str,
        api_timeout: int,
    ) -> bool:
        suffix: str = "user/repos"
        if account_type == "org":
            suffix = f"orgs/{account}/repos"
        url: str = f"{self.api_base}/{suffix}"
        response: requests.Response = session.post(
            url,
            headers={"Content-Type": "application/json;charset=UTF-8"},
            params={"name": repo_name, "access_token": token},
            timeout=api_timeout,
        )
        if response.status_code == 201:
            logger.info("Destination repo creating accepted.")
            return True
        logger.error(f"Destination repo creating failed: {response.text}")
        return False


class GitLabPlatform(GitPlatform):
    name = "gitlab"
    repo_field = "projects"

    def __init__(self, endpoint: str = "") -> None:
        host = endpoint or "gitlab.com"
        self.host: str = host
        self.api_base: str = f"https://{host}/api/v4"

    def validate_account_type(self, account_type: str, role: str) -> None:
        self._validate_account_type(account_type, role, ("user", "group"))

    def create_repo(
        self,
        session: requests.Session,
        account: str,
        account_type: str,
        repo_name: str,
        token: str,
        api_timeout: int,
    ) -> bool:
        url: str = f"{self.api_base}/{self.repo_field}"
        headers: Dict[str, str] = {"PRIVATE-TOKEN": token}
        data: Dict[str, Any] = {"name": repo_name, "visibility": "public"}
        if account_type == "group":
            group_id: Optional[int] = self._get_group_id(
                session, account, token, api_timeout
            )
            data["namespace_id"] = group_id
        response: requests.Response = session.post(
            url,
            data=data,
            headers=headers,
            timeout=api_timeout,
        )
        if response.status_code == 201:
            logger.info("Destination repo creating accepted.")
            return True
        logger.error(f"Destination repo creating failed: {response.text}")
        return False

    def _get_group_id(
        self,
        session: requests.Session,
        group_name: str,
        token: str,
        api_timeout: int,
    ) -> Optional[int]:
        url: str = f"{self.api_base}/groups"
        headers: Dict[str, str] = {"PRIVATE-TOKEN": token}
        response: requests.Response = session.get(
            url, headers=headers, timeout=api_timeout
        )
        if response.status_code == 200:
            groups: List[Dict[str, Any]] = response.json()
            for group in groups:
                if group.get("path") == group_name:
                    return group.get("id")
            logger.warning(f"Failed to find group ID for '{group_name}'.")
        else:
            logger.error("Failed to get groups list.")
            logger.error(f"Error message: {response.text}")
        return None


def get_platform(name: str, endpoint: str = "") -> GitPlatform:
    platforms: Dict[str, Type[GitPlatform]] = {
        "github": GitHubPlatform,
        "gitee": GiteePlatform,
        "gitlab": GitLabPlatform,
        "gitcode": GitcodePlatform,
    }
    platform_cls = platforms.get(name)
    if not platform_cls:
        supported = ", ".join(sorted(platforms.keys()))
        raise ValueError(f"Unsupported platform_type '{name}'. Supported: {supported}")
    return platform_cls(endpoint)
