import logging
import os
import re
import shutil
from typing import List

import git
from tenacity import retry, stop_after_attempt, wait_exponential

from utils import cov2sec

logger = logging.getLogger(__name__)


class Mirror(object):
    def __init__(
        self,
        hub: "Hub",
        src_name: str,
        dst_name: str,
        cache: str = ".",
        timeout: str = "0",
        force_update: bool = False,
        lfs: bool = False,
    ) -> None:
        self.hub: "Hub" = hub
        self.src_name: str = src_name
        self.dst_name: str = dst_name
        self.src_url: str = hub.src_repo_base + "/" + src_name + ".git"
        self.dst_url: str = hub.dst_repo_base + "/" + dst_name + ".git"
        self.repo_path: str = os.path.join(cache, src_name)
        self.timeout: int = 0
        if re.match(r"^\d+[dhms]?$", timeout):
            self.timeout = cov2sec(timeout)
        self.force_update: bool = force_update
        self.lfs: bool = lfs

    @retry(wait=wait_exponential(), reraise=True, stop=stop_after_attempt(3))
    def _clone(self) -> None:
        # TODO: process empty repo
        logger.info(f"Starting git clone {self.src_url}")
        mygit: git.cmd.Git = git.cmd.Git(os.getcwd())
        mygit.clone(
            git.cmd.Git.polish_url(self.src_url),
            self.repo_path,
            kill_after_timeout=self.timeout,
        )
        local_repo: git.Repo = git.Repo(self.repo_path)
        if self.lfs:
            local_repo.git.lfs("fetch", "--all", "origin")
        logger.info(f"Clone completed: {os.getcwd() + self.repo_path}")

    @retry(wait=wait_exponential(), reraise=True, stop=stop_after_attempt(3))
    def _update(self, local_repo: git.Repo) -> None:
        try:
            local_repo.git.pull(kill_after_timeout=self.timeout)
            if self.lfs:
                local_repo.git.lfs("fetch", "--all", "origin")
        except git.exc.GitCommandError:
            # Cleanup local repo and re-clone
            logger.warning(f"Updating failed, re-clone {self.src_name}")
            shutil.rmtree(local_repo.working_dir)
            self._clone()

    @retry(wait=wait_exponential(), reraise=True, stop=stop_after_attempt(3))
    def download(self) -> None:
        logger.info("(1/3) Downloading...")
        try:
            local_repo: git.Repo = git.Repo(self.repo_path)
        except git.exc.NoSuchPathError:
            self._clone()
        else:
            logger.info("Updating repo...")
            self._update(local_repo)

    def create(self) -> None:
        logger.info("(2/3) Creating...")
        self.hub.create_dst_repo(self.dst_name)

    def _check_empty(self, repo: git.Repo) -> bool:
        cmd: List[str] = ["-n", "1", "--all"]
        if repo.git.rev_list(*cmd):
            return False
        return True

    @retry(wait=wait_exponential(), reraise=True, stop=stop_after_attempt(3))
    def push(self, force: bool = False) -> None:
        local_repo: git.Repo = git.Repo(self.repo_path)
        git_cmd: git.cmd.Git = local_repo.git
        if self._check_empty(local_repo):
            logger.info(f"Empty repo {self.src_url}, skip pushing.")
            return
        cmd: List[str] = ["set-head", "origin", "-d"]
        local_repo.git.remote(*cmd)
        try:
            local_repo.create_remote(self.hub.dst_type, self.dst_url)
        except git.exc.GitCommandError:
            logger.info(
                f"Remote exists, re-create: set {self.hub.dst_type} "
                f"to {self.dst_url}"
            )
            local_repo.delete_remote(self.hub.dst_type)
            local_repo.create_remote(self.hub.dst_type, self.dst_url)
        cmd = [
            self.hub.dst_type,
            "refs/remotes/origin/*:refs/heads/*",
            "--tags",
            "--prune",
        ]
        if not self.force_update:
            logger.info("(3/3) Pushing...")
            local_repo.git.push(*cmd, kill_after_timeout=self.timeout)
            if self.lfs:
                git_cmd.lfs("push", self.hub.dst_type, "--all")
        else:
            logger.info("(3/3) Force pushing...")
            if self.lfs:
                git_cmd.lfs("push", self.hub.dst_type, "--all")
            cmd = ["-f"] + cmd
            local_repo.git.push(*cmd, kill_after_timeout=self.timeout)
