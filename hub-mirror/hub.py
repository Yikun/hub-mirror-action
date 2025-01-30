import time
import functools
import json

import requests


class Hub(object):
    def __init__(
        self, src, dst, dst_token, account_type="user",
        clone_style="https",
        src_account_type=None,
        dst_account_type=None,
        api_timeout=60,
    ):
        self.api_timeout = api_timeout
        self.account_type = account_type
        self.src_account_type = src_account_type or account_type
        self.dst_account_type = dst_account_type or account_type
        self.src_type, self.src_account = src.split('/')
        self.dst_type, self.dst_account = dst.split('/')
        self._validate_account_type(
            self.src_type, self.src_account_type, 'source'
        )
        self._validate_account_type(
            self.dst_type, self.dst_account_type, 'destination'
        )
        self.dst_token = dst_token
        self.session = requests.Session()
        if self.dst_type == "gitee":
            self.dst_base = 'https://gitee.com/api/v5'
        elif self.dst_type == "github":
            self.dst_base = 'https://api.github.com'
        elif self.dst_type == "gitlab":
            self.dst_base = 'https://gitlab.com/api/v4'

        prefix = "https://" if clone_style == 'https' else 'git@'
        suffix = "/" if clone_style == 'https' else ':'
        if self.src_type == "gitee":
            self.src_base = 'https://gitee.com/api/v5'
            self.src_repo_base = prefix + 'gitee.com' + suffix
        elif self.src_type == "github":
            self.src_base = 'https://api.github.com'
            self.src_repo_base = prefix + 'github.com' + suffix
        elif self.src_type == "gitlab":
            self.src_base = 'https://gitlab.com/api/v4'
            self.src_repo_base = prefix + 'gitlab.com' + suffix
        self.src_repo_base = self.src_repo_base + self.src_account
        # TODO: toekn push support
        prefix = "git@" + self.dst_type + ".com:"
        self.dst_repo_base = prefix + self.dst_account

    def _validate_account_type(self, platform_type, account_type, role):
        if platform_type not in ("gitlab", "github", "gitee"):
            raise ValueError(
                f"Unsupported platform_type '{platform_type}' for {role}."
            )
        # gitlab ---> user or group
        if platform_type == "gitlab":
            if account_type not in ("user", "group"):
                raise ValueError(
                    f"For {platform_type}, {role} account_type must be "
                    "either 'user' or 'group'."
                )
        # github/gitee ---> user or org
        elif platform_type in ("github", "gitee"):
            if account_type not in ("user", "org"):
                raise ValueError(
                    f"For {platform_type}, {role} account_type must be"
                    "either 'user' or 'org'."
                )

    def has_dst_repo(self, repo_name):
        # gitlab ---> projects, github/gitee ---> repos
        repo_field = "projects" if self.dst_type == "gitlab" else "repos"
        url = '/'.join(
            [
                self.dst_base, self.dst_account_type+'s', self.dst_account,
                repo_field,
            ]
        )
        repo_names = self._get_all_repo_names(url)
        if not repo_names:
            print("Warning: destination repos is []")
            return False
        return repo_name in repo_names

    def create_dst_repo(self, repo_name):
        # gitlab ---> projects, github/gitee ---> repos
        repo_field = "projects" if self.dst_type == "gitlab" else "repos"
        if self.dst_type == "gitlab":
            url = f"{self.dst_base}/{repo_field}"
            headers = {'PRIVATE-TOKEN': self.dst_token}
            data = {'name': repo_name, 'visibility': 'public'}
            # If creating under a group, add namespace_id
            if self.dst_account_type == "group":
                group_id = self._get_gitlab_group_id(self.dst_account)
                data['namespace_id'] = group_id
        else:
            suffix = f"user/{repo_field}"
            if self.dst_account_type == "org":
                suffix = f"orgs/{self.dst_account}/{repo_field}"
            url = '/'.join(
                [self.dst_base, suffix]
            )
            result = None
            if self.dst_type == 'gitee':
                data = {'name': repo_name}
            elif self.dst_type == 'github':
                data = json.dumps({'name': repo_name})
        if not self.has_dst_repo(repo_name):
            print(repo_name + " doesn't exist, create it...")
            if self.dst_type == "github":
                response = self.session.post(
                    url,
                    data=data,
                    headers={'Authorization': 'token ' + self.dst_token},
                    timeout=self.api_timeout
                )
                result = response.status_code == 201
                if result:
                    print("Destination repo creating accepted.")
                else:
                    print("Destination repo creating failed: " + response.text)
            elif self.dst_type == "gitee":
                response = requests.post(
                    url,
                    headers={'Content-Type': 'application/json;charset=UTF-8'},
                    params={"name": repo_name, "access_token": self.dst_token},
                    timeout=self.api_timeout
                )
                result = response.status_code == 201
                if result:
                    print("Destination repo creating accepted.")
                else:
                    print("Destination repo creating failed: " + response.text)
            elif self.dst_type == "gitlab":
                response = self.session.post(
                    url,
                    data=data,
                    headers=headers,
                    timeout=self.api_timeout
                )
                result = response.status_code == 201
                if result:
                    print("Destination repo creating accepted.")
                else:
                    print("Destination repo creating failed: " + response.text)
        else:
            print(repo_name + " repo exist, skip creating...")
        # TODO(snowyu): Cleanup 2s sleep
        if result:
            time.sleep(2)
        return result

    def dynamic_list(self):
        # gitlab ---> projects, github/gitee ---> repos
        repo_field = "projects" if self.src_type == "gitlab" else "repos"
        url = '/'.join(
            [
                self.src_base, self.src_account_type + 's', self.src_account,
                repo_field,
            ]
        )
        return self._get_all_repo_names(url)

    @functools.lru_cache
    def _get_all_repo_names(self, url, page=1):
        per_page = 60
        api = url + f"?page={page}&per_page=" + str(per_page)
        # TODO: src_token support
        response = self.session.get(api, timeout=self.api_timeout)
        all_items = []
        if response.status_code != 200:
            print("Repo getting failed: " + response.text)
            return all_items
        items = response.json()
        if items:
            names = [i['name'] for i in items]
            return names + self._get_all_repo_names(url, page=page+1)
        return all_items

    def _get_gitlab_group_id(self, group_name):
        """Helper method to get GitLab group ID"""
        url = f"{self.dst_base}/groups"
        headers = {'PRIVATE-TOKEN': self.dst_token}
        response = self.session.get(
            url,
            headers=headers,
            timeout=self.api_timeout
        )
        if response.status_code == 200:
            groups = response.json()
            for group in groups:
                if group['path'] == group_name:
                    return group['id']
            print(f"Failed to find group ID for '{group_name}'.")
        else:
            print("Failed to get groups list.")
            print(f"Error message: {response.text}")
        return None
