#!/bin/bash

set -x
mkdir -p /root/.ssh
echo "${INPUT_DST_KEY}" > /root/.ssh/id_rsa
chmod 600 /root/.ssh/id_rsa

DST_TOKEN="${INPUT_DST_TOKEN}"

SRC_HUB="${INPUT_SRC}"
DST_HUB="${INPUT_DST}"

ACCOUNT_TYPE="${INPUT_ACCOUNT_TYPE}"

SRC_TYPE=`dirname $SRC_HUB`
DST_TYPE=`dirname $DST_HUB`

SRC_ACCOUNT=`basename $SRC_HUB`
DST_ACCOUNT=`basename $DST_HUB`

CLONE_STYLE="${INPUT_CLONE_STYLE}"

CACHE_PATH="${INPUT_CACHE_PATH}"

if [[ "$ACCOUNT_TYPE" == "org" ]]; then
  SRC_LIST_URL_SUFFIX=orgs/$SRC_ACCOUNT/repos
  DST_LIST_URL_SUFFIX=orgs/$DST_ACCOUNT/repos
  DST_CREATE_URL_SUFFIX=orgs/$DST_ACCOUNT/repos
elif [[ "$ACCOUNT_TYPE" == "user" ]]; then
  SRC_LIST_URL_SUFFIX=users/$SRC_ACCOUNT/repos
  DST_LIST_URL_SUFFIX=users/$DST_ACCOUNT/repos
  DST_CREATE_URL_SUFFIX=user/repos
else
  echo "Unknown account type, the `account_type` should be `user` or `org`"
  exit 1
fi

if [[ "$SRC_TYPE" == "github" ]]; then
  SRC_REPO_LIST_API=https://api.github.com/$SRC_LIST_URL_SUFFIX
  if [[ "$CLONE_STYLE" == "ssh" ]]; then
    SRC_REPO_BASE_URL=git@github.com:
  elif [[ "$CLONE_STYLE" == "https" ]]; then
    SRC_REPO_BASE_URL=https://github.com/
  fi
elif [[ "$SRC_TYPE" == "gitee" ]]; then
  SRC_REPO_LIST_API=https://gitee.com/api/v5/$SRC_LIST_URL_SUFFIX
  if [[ "$CLONE_STYLE" == "ssh" ]]; then
    SRC_REPO_BASE_URL=git@gitee.com:
  elif [[ "$CLONE_STYLE" == "https" ]]; then
    SRC_REPO_BASE_URL=https://gitee.com/
  fi
else
  echo "Unknown src args, the `src` should be `[github|gittee]/account`"
  exit 1
fi

SRC_REPOS=`curl $SRC_REPO_LIST_API | jq '.[] | .name' |  sed 's/"//g'`

if [[ "$DST_TYPE" == "github" ]]; then
  DST_REPO_CREATE_API=https://api.github.com/$DST_CREATE_URL_SUFFIX
  DST_REPO_LIST_API=https://api.github.com/$DST_LIST_URL_SUFFIX
elif [[ "$DST_TYPE" == "gitee" ]]; then
  DST_REPO_CREATE_API=https://gitee.com/api/v5/$DST_CREATE_URL_SUFFIX
  DST_REPO_LIST_API=https://gitee.com/api/v5/$DST_LIST_URL_SUFFIX
else
  echo "Unknown dst args, the `dst` should be `[github|gittee]/account`"
  exit 1
fi


function cd_src_repo
{
  echo -e "\033[31m(0/3)\033[0m" "Downloading..."
  if [ ! -d "$1" ]; then
    git clone $SRC_REPO_BASE_URL$SRC_ACCOUNT/$1.git
  fi
  cd $1
}

function add_remote_repo
{
  # Auto create non-existing repo
  has_repo=`curl $DST_REPO_LIST_API | jq '.[] | select(.full_name=="'$DST_ACCOUNT'/'$1'").name' | wc -l`
  if [ $has_repo == 0 ]; then
    if [[ "$DST_TYPE" == "github" ]]; then
      curl -H "Authorization: token $2" --data '{"name":"'$1'"}' $DST_REPO_CREATE_API
    elif [[ "$DST_TYPE" == "gitee" ]]; then
      curl -X POST --header 'Content-Type: application/json;charset=UTF-8' $DST_REPO_CREATE_API -d '{"name": "'$1'","access_token": "'$2'"}'
    fi
  fi
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

if [ ! -d "$CACHE_PATH" ]; then
  mkdir -p $CACHE_PATH
fi
cd $CACHE_PATH

for repo in $SRC_REPOS
{
  echo -e "\n\033[31mBackup $repo ...\033[0m"

  cd_src_repo $repo

  add_remote_repo $repo $DST_TOKEN

  update_repo

  if [ $? -eq 0 ]; then
    import_repo
  else
    echo -e "\033[31mUpdate failed.\033[0m" ""
  fi

  cd ..
}

