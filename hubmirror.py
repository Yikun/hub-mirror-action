import argparse
import functools
import json
import re
import shutil
import sys
import yaml
import os

import git
import requests
from tenacity import retry, stop_after_attempt, wait, wait_exponential


class Progress(git.remote.RemoteProgress):
    def __init__(self, name):
        super(Progress, self).__init__()
        self.name = name

    def update(self, op_code, cur_count, max_count=None, message=''):
        print('Process %s, %s' % (self.name, self._cur_line))

# TODO: move to utils
def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

# TODO: move to utils
def cov2sec(s):
    _h = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
    if _h.get(s[-1]):
        return int(s[:-1]) * _h.get(s[-1], 1)
    else:
        return int(s)

# class for repo git related work
class Mirror(object):
    def __init__(self, hub, name, cache='.', timeout='0', force_update=False):
        self.hub = hub
        self.name = name
        self.src_url = hub.src_repo_base + '/' +name + ".git"
        self.dst_url = hub.dst_repo_base + '/' +name + ".git"
        self.repo_path = cache + '/' + name
        if re.match("^\d+[dhms]?$", timeout):
            self.timeout = cov2sec(timeout)
        else:
            self.timeout = 0
        self.force_update = force_update

    @retry(wait=wait_exponential(), reraise=True, stop=stop_after_attempt(3))
    def _clone(self):
        # TODO: process empty repo
        print("Starting git clone " + self.src_url)
        mygit = git.cmd.Git(os.getcwd())
        mygit.clone(
            git.cmd.Git.polish_url(self.src_url), self.repo_path,
            kill_after_timeout=self.timeout
        )
        print("Clone completed: %s" % os.getcwd() + self.repo_path)

    @retry(wait=wait_exponential(), reraise=True, stop=stop_after_attempt(3))
    def _update(self, local_repo):
        try:
            local_repo.git.pull(kill_after_timeout=self.timeout)
        except git.exc.GitCommandError:
            # Cleanup local repo and re-clone
            print('Updating failed, re-clone %s' % self.name)
            shutil.rmtree(local_repo.working_dir)
            self._clone()

    @retry(wait=wait_exponential(), reraise=True, stop=stop_after_attempt(3))
    def download(self):
        print("(1/3) Downloading...")
        try:
            local_repo = git.Repo(self.repo_path)
        except git.exc.NoSuchPathError:
            self._clone()
        else:
            print("Updating repo...")
            self._update(local_repo)

    def create(self):
        print("(2/3) Creating...")
        self.hub.create_dst_repo(self.name)

    @retry(wait=wait_exponential(), reraise=True, stop=stop_after_attempt(3))
    def push(self, force=False):
        local_repo = git.Repo(self.repo_path)
        cmd = ['set-head', 'origin', '-d']
        local_repo.git.remote(*cmd)
        try:
            local_repo.create_remote(self.hub.dst_type, self.dst_url)
        except git.exc.GitCommandError as e:
            print("Remote exsits, re-create: set %s to %s" % (
                self.hub.dst_type, self.dst_url))
            local_repo.delete_remote(self.hub.dst_type)
            local_repo.create_remote(self.hub.dst_type, self.dst_url)
        cmd = [self.hub.dst_type, 'refs/remotes/origin/*:refs/heads/*', '--tags', '--prune']
        if not self.force_update:
            print("(3/3) Pushing...")
            local_repo.git.push(*cmd, kill_after_timeout=self.timeout)
        else:
            print("(3/3) Force pushing...")
            cmd = ['-f'] + cmd
            local_repo.git.push(*cmd, kill_after_timeout=self.timeout)


# class for hub api related work
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
        self.dst_repo_base = "git@" + self.dst_type + ".com:" + self.dst_account

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
        page, total, per_page = 1, 0, 60
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


class HubMirror(object):
    def __init__(self):
        self.parser = self._create_parser()
        self.args = self.parser.parse_args()

        # Change "a, b" to ['a', 'b']
        _cov = lambda x: x.replace(' ', '').split(',') if x else []
        self.white_list = _cov(self.args.white_list)
        self.black_list = _cov(self.args.black_list)
        self.static_list = _cov(self.args.static_list)

    def _create_parser(self):
        with open('/action.yml', 'r') as f:
            action = yaml.safe_load(f)
        parser = argparse.ArgumentParser(
            description=action['description'])
        inputs = action['inputs']

        for key in inputs:
            if key in ['dst_key']:
                continue
            input_args = inputs[key]
            dft = input_args.get('default', '')
            parser.add_argument(
                "--" + key.replace('_', '-'),
                # Autofill the `type` according `default`, str by default
                type=str2bool if isinstance(dft, bool) else str,
                required=input_args.get('required', False),
                default=dft,
                help=input_args.get('description', '')
            )
        return parser

    def test_black_white_list(self, repo):
        if repo in self.black_list:
            print("Skip, %s in black list: %s" % (repo, self.black_list))
            return False

        if self.white_list and repo not in self.white_list:
            print("Skip, %s not in white list: %s" % (repo, self.white_list))
            return False

        return True

    def run(self):
        hub = Hub(
            self.args.src,
            self.args.dst,
            self.args.dst_token,
            account_type=self.args.account_type,
            clone_style=self.args.clone_style
        )
        src_type, src_account = self.args.src.split('/')

        # Using static list when static_list is set
        repos = self.args.static_list
        src_repos =  repos.split(',') if repos else hub.dynamic_list()

        total, success, skip = len(src_repos), 0, 0
        failed_list = []
        for repo in src_repos:
            if self.test_black_white_list(repo):
                print("Backup %s" % repo)
                try:
                    mirror = Mirror(
                        hub, repo,
                        cache=self.args.cache_path,
                        timeout=self.args.timeout,
                        force_update=self.args.force_update,
                    )
                    mirror.download()
                    mirror.create()
                    mirror.push()
                    success += 1
                except Exception as e:
                    print(e)
                    failed_list.append(repo)
            else:
                skip += 1
        failed = total - success - skip
        res = (total, skip, success, failed)
        print("Total: %s, skip: %s, successed: %s, failed: %s." % res)
        print("Failed: %s" % failed_list)
        if failed_list:
            sys.exit(1)


if __name__ == '__main__':
    mirror = HubMirror()
    mirror.run()