#!/bin/bash

set -x
mkdir -p /root/.ssh
echo "${INPUT_DST_KEY}" > /root/.ssh/id_rsa
chmod 600 /root/.ssh/id_rsa

SRC_HUB="${INPUT_SRC}"
DST_HUB="${INPUT_DST}"

SRC_TYPE=`dirname $SRC_HUB`
DST_TYPE=`dirname $DST_HUB`

SRC_ACCOUNT=`basename $SRC_HUB`
DST_ACCOUNT=`basename $DST_HUB`

if [[ "$SRC_TYPE" == "github" ]]; then
  SRC_REPO_LIST_API=https://api.github.com/orgs/$SRC_ACCOUNT/repos
  SRC_REPO_BASE_URL=https://github.com
elif [[ "$SRC_TYPE" == "gitee" ]]; then
  SRC_REPO_LIST_API=https://gitee.com/api/v5/orgs/$SRC_ACCOUNT/repos
  SRC_REPO_BASE_URL=https://gitee.com
else
  echo "Unknown src args, the `src` should be `[github|gittee]/account`"
  exit 1
fi

SRC_REPOS=`curl $SRC_REPO_LIST_API | jq '.[] | .name' |  sed 's/"//g'`

if [[ "$DST_TYPE" == "github" ]]; then
  DST_REPO_API=https://api.github.com/orgs/$DST_ACCOUNT/repos
elif [[ "$DST_TYPE" == "gitee" ]]; then
  DST_REPO_API=https://gitee.com/api/v5/orgs/$DST_ACCOUNT/repos
else
  echo "Unknown dst args, the `dst` should be `[github|gittee]/account`"
  exit 1
fi


function cd_src_repo
{
  echo -e "\033[31m(0/3)\033[0m" "Downloading..."
  if [ ! -d "$1" ]; then
    git clone $SRC_REPO_BASE_URL/$SRC_ACCOUNT/$1.git
  fi
  cd $1
}

function add_remote_repo
{
  git remote add $DST_TYPE git@$DST_TYPE.com:$DST_ACCOUNT/$1.git
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
  git push $DST_TYPE refs/remotes/origin/*:refs/heads/* --tags --prune
}

for repo in $SRC_REPOS
{
  echo -e "\n\033[31mBackup $repo ...\033[0m"

  cd_src_repo $repo

  add_remote_repo $repo

  update_repo

  if [ $? -eq 0 ]; then
    import_repo
  else
    echo -e "\033[31mUpdate failed.\033[0m" ""
  fi

  cd ..
}

