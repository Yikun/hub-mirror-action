import functools
import json

import requests


class Hub(object):
    def __init__(
        self, src, dst, dst_token, account_type="user",
        clone_style="https"
    ):
        # TODO: check invalid type
        self.account_type = account_type
        self.src_type, self.src_account = src.split('/')
        self.dst_type, self.dst_account = dst.split('/')
        self.dst_token = dst_token
        self.session = requests.Session()
        if self.dst_type == "gitee":
            self.dst_base = 'https://gitee.com/api/v5'
        elif self.dst_type == "github":
            self.dst_base = 'https://api.github.com'

        prefix = "https://" if clone_style == 'https' else 'git@'
        suffix = "/" if clone_style == 'https' else ':'
        if self.src_type == "gitee":
            self.src_base = 'https://gitee.com/api/v5'
            self.src_repo_base = prefix + 'gitee.com' + suffix
        elif self.src_type == "github":
            self.src_base = 'https://api.github.com'
            self.src_repo_base = prefix + 'github.com' + suffix
        self.src_repo_base = self.src_repo_base + self.src_account
        # TODO: toekn push support
        prefix = "git@" + self.dst_type + ".com:"
        self.dst_repo_base = prefix + self.dst_account

    def has_dst_repo(self, repo_name):
        url = '/'.join(
            [self.dst_base, self.account_type+'s', self.dst_account, 'repos']
        )
        repo_names = self._get_all_repo_names(url)
        if not repo_names:
            print("Warning: destination repos is []")
            return False
        return repo_name in repo_names

    def create_dst_repo(self, repo_name):
        suffix = 'user/repos'
        if self.account_type == "org":
            suffix = 'orgs/%s/repos' % self.dst_account
        url = '/'.join(
            [self.dst_base, suffix]
        )
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
                    headers={'Authorization': 'token ' + self.dst_token}
                )
                if response.status_code == 201:
                    print("Destination repo creating accepted.")
                else:
                    print("Destination repo creating failed: " + response.text)
            elif self.dst_type == "gitee":
                response = requests.post(
                    url,
                    headers={'Content-Type': 'application/json;charset=UTF-8'},
                    params={"name": repo_name, "access_token": self.dst_token}
                )
                if response.status_code == 201:
                    print("Destination repo creating accepted.")
                else:
                    print("Destination repo creating failed: " + response.text)
        else:
            print(repo_name + " repo exist, skip creating...")

    def dynamic_list(self):
        url = '/'.join(
            [self.src_base, self.account_type+'s', self.src_account, 'repos']
        )
        return self._get_all_repo_names(url)

    @functools.lru_cache
    def _get_all_repo_names(self, url):
        page, per_page = 1, 60
        api = url + "?page=0&per_page=" + str(per_page)
        # TODO: src_token support
        response = self.session.get(api)
        # TODO: DRY
        if response.status_code != 200:
            print("Repo getting failed: " + response.text)
            return []
        items = response.json()
        all_items = []
        while items:
            names = [i['name'] for i in items]
            all_items += names
            items = None
            if 'next' in response.links:
                url_next = response.links['next']['url']
                response = self.session.get(url_next)
                # TODO: DRY
                if response.status_code != 200:
                    print("Repo getting failed: " + response.text)
                    return []
                page += 1
                items = response.json()

        return all_items
