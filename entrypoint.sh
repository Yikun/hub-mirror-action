#!/bin/bash

set -x
mkdir -p /root/.ssh
echo "${INPUT_PRIVATE_KEY}" > /root/.ssh/id_rsa
chmod 600 /root/.ssh/id_rsa

repos=`curl https://api.github.com/orgs/kunpengcompute/repos | jq '.[] | .name' |  sed 's/"//g'`
github_org="${INPUT_GITHUB_ORG}"
gitee_org="${INPUT_GITEE_ORG}"

function clone_and_cd_repo
{
  echo -e "\033[31m(0/3)\033[0m" "Downloading..."
  if [ ! -d "$2" ]; then
    git clone https://github.com/$1/$2.git
    cd $2
    git remote add gitee git@gitee.com:$gitee_org/$2.git
  else
    cd $2
  fi
}

function update_repo
{
  echo -e "\033[31m(1/3)\033[0m" "Updating..."
  git pull -p
}

function import_repo
{
  echo -e "\033[31m(2/3)\033[0m" "Importing..."
  git remote set-head origin -d
  git push gitee refs/remotes/origin/*:refs/heads/* --tags --prune
}

for repo in $repos
{
  echo -e "\n\033[31mBackup $repo ...\033[0m"

  clone_and_cd_repo $github_org $repo

  update_repo

  if [ $? -eq 0 ]; then
    import_repo
  else
    echo -e "\033[31mUpdate failed.\033[0m" ""
  fi

  cd ..
}
