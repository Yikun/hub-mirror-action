import re
import shutil
import os

import git
from tenacity import retry, stop_after_attempt, wait_exponential

from utils import cov2sec


class Mirror(object):
    def __init__(
        self, hub, src_name, dst_name,
        cache='.', timeout='0', force_update=False, lfs=False
    ):
        self.hub = hub
        self.src_name = src_name
        self.dst_name = dst_name
        self.src_url = hub.src_repo_base + '/' + src_name + ".git"
        self.dst_url = hub.dst_repo_base + '/' + dst_name + ".git"
        self.repo_path = cache + '/' + src_name
        if re.match(r"^\d+[dhms]?$", timeout):
            self.timeout = cov2sec(timeout)
        else:
            self.timeout = 0
        self.force_update = force_update
        self.lfs = lfs

    @retry(wait=wait_exponential(), reraise=True, stop=stop_after_attempt(3))
    def _clone(self):
        # TODO: process empty repo
        print("Starting git clone " + self.src_url)
        mygit = git.cmd.Git(os.getcwd())
        mygit.clone(
            git.cmd.Git.polish_url(self.src_url), self.repo_path,
            kill_after_timeout=self.timeout
        )
        local_repo = git.Repo(self.repo_path)
        if self.lfs:
            local_repo.git.lfs("fetch", "--all", "origin")
        print("Clone completed: %s" % (os.getcwd() + self.repo_path))

    @retry(wait=wait_exponential(), reraise=True, stop=stop_after_attempt(3))
    def _update(self, local_repo):
        try:
            local_repo.git.pull(kill_after_timeout=self.timeout)
            if self.lfs:
                local_repo.git.lfs("fetch", "--all", "origin")
        except git.exc.GitCommandError:
            # Cleanup local repo and re-clone
            print('Updating failed, re-clone %s' % self.src_name)
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
        self.hub.create_dst_repo(self.dst_name)

    def _check_empty(self, repo):
        cmd = ["-n", "1", "--all"]
        if repo.git.rev_list(*cmd):
            return False
        else:
            return True

    @retry(wait=wait_exponential(), reraise=True, stop=stop_after_attempt(3))
    def push(self, force=False):
        local_repo = git.Repo(self.repo_path)
        git_cmd = local_repo.git
        if self._check_empty(local_repo):
            print("Empty repo %s, skip pushing." % self.src_url)
            return
        cmd = ['set-head', 'origin', '-d']
        local_repo.git.remote(*cmd)
        try:
            local_repo.create_remote(self.hub.dst_type, self.dst_url)
        except git.exc.GitCommandError:
            print("Remote exists, re-create: set %s to %s" % (
                self.hub.dst_type, self.dst_url))
            local_repo.delete_remote(self.hub.dst_type)
            local_repo.create_remote(self.hub.dst_type, self.dst_url)
        cmd = [
            self.hub.dst_type, 'refs/remotes/origin/*:refs/heads/*',
            '--tags', '--prune'
        ]
        if not self.force_update:
            print("(3/3) Pushing...")
            local_repo.git.push(*cmd, kill_after_timeout=self.timeout)
            if self.lfs:
                git_cmd.lfs("push", self.hub.dst_type, "--all")
        else:
            print("(3/3) Force pushing...")
            if self.lfs:
                git_cmd.lfs("push", self.hub.dst_type, "--all")
            cmd = ['-f'] + cmd
            local_repo.git.push(*cmd, kill_after_timeout=self.timeout)
