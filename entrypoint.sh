#!/bin/bash

DEBUG="${INPUT_DEBUG}"

if [[ "$DEBUG" == "true" ]]; then
  set -x
fi

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

WHITE_LIST="${INPUT_WHITE_LIST}"
BLACK_LIST="${INPUT_BLACK_LIST}"
STATIC_LIST="${INPUT_STATIC_LIST}"

FORCE_UPDATE="${INPUT_FORCE_UPDATE}"

DELAY_EXIT=false

TIME_OUT="${INPUT_TIMEOUT}"
RETRY_TIMES=3

function err_exit {
  echo -e "\033[31m $1 \033[0m"
  exit 1
}

FAILED_LIST=()

function delay_exit {
  echo -e "\033[31m $1 \033[0m"
  FAILED_LIST+=($2)
  DELAY_EXIT=true
  return 1
}

if [[ "$ACCOUNT_TYPE" == "org" ]]; then
  SRC_LIST_URL_SUFFIX=orgs/$SRC_ACCOUNT/repos
  DST_LIST_URL_SUFFIX=orgs/$DST_ACCOUNT/repos
  DST_CREATE_URL_SUFFIX=orgs/$DST_ACCOUNT/repos
elif [[ "$ACCOUNT_TYPE" == "user" ]]; then
  SRC_LIST_URL_SUFFIX=users/$SRC_ACCOUNT/repos
  DST_LIST_URL_SUFFIX=users/$DST_ACCOUNT/repos
  DST_CREATE_URL_SUFFIX=user/repos
else
  err_exit "Unknown account type, the `account_type` should be `user` or `org`"
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
  err_exit "Unknown src args, the `src` should be `[github|gittee]/account`"
fi

function retry {
  local retries=$RETRY_TIMES
  local count=0
  until timeout $TIME_OUT "$@"; do
    exit=$?
    wait=$((2 ** $count))
    count=$(($count + 1))
    if [ $count -lt $retries ]; then
      echo "Retry $count/$retries exited $exit, retrying in $wait seconds..."
      sleep $wait
    else
      echo "Retry $count/$retries exited $exit, no more retries left."
      return $exit
    fi
  done
  return 0
}

function get_all_repo_names
{
  PAGE_NUM=100
  URL=$1
  HUB_TYPE=$2
  if [[ "$HUB_TYPE" == "github" ]]; then
    total=`curl -sI "$URL?page=1&per_page=$PAGE_NUM" | sed -nr "s/^[lL]ink:.*page=([0-9]+)&per_page=$PAGE_NUM.*/\1/p"`
  elif [[ "$HUB_TYPE" == "gitee" ]]; then
    total=`curl -sI "$URL?page=1&per_page=$PAGE_NUM" | grep total_page: |cut -d ' ' -f2 |tr -d '\r'`
  fi

  # use pagination?
  if [ -z "$total" ]; then
      # no - this result has only one page
      total=1
  fi

  p=1
  while [ "$p" -le "$total" ]; do
    x=`curl -s "$URL?page=$p&per_page=$PAGE_NUM" | jq '.[] | .name' |  sed 's/"//g'`
    echo $x
    p=$(($p + 1))
  done
}

if [[ -z $STATIC_LIST ]]; then
  SRC_REPOS=`get_all_repo_names $SRC_REPO_LIST_API $SRC_TYPE`
else
  SRC_REPOS=`echo $STATIC_LIST | tr ',' ' '`
fi

if [[ "$DST_TYPE" == "github" ]]; then
  DST_REPO_CREATE_API=https://api.github.com/$DST_CREATE_URL_SUFFIX
  DST_REPO_LIST_API=https://api.github.com/$DST_LIST_URL_SUFFIX
elif [[ "$DST_TYPE" == "gitee" ]]; then
  DST_REPO_CREATE_API=https://gitee.com/api/v5/$DST_CREATE_URL_SUFFIX
  DST_REPO_LIST_API=https://gitee.com/api/v5/$DST_LIST_URL_SUFFIX
else
  err_exit "Unknown dst args, the `dst` should be `[github|gittee]/account`"
fi

DST_REPOS=`get_all_repo_names $DST_REPO_LIST_API $DST_TYPE`

function clone_repo
{
  echo -e "\033[31m(0/3)\033[0m" "Downloading..."
  if [ ! -d "$1" ]; then
    retry git clone $SRC_REPO_BASE_URL$SRC_ACCOUNT/$1.git
  fi
  cd $1
}

function create_repo
{
  # Auto create non-existing repo
  has_repo=`echo $DST_REPOS | grep -w $1 | wc -l`
  if [ $has_repo == 0 ]; then
    echo "Create non-exist repo..."
    if [[ "$DST_TYPE" == "github" ]]; then
      curl -s -H "Authorization: token $2" --data '{"name":"'$1'"}' $DST_REPO_CREATE_API > /dev/null
    elif [[ "$DST_TYPE" == "gitee" ]]; then
      curl -s -X POST --header 'Content-Type: application/json;charset=UTF-8' $DST_REPO_CREATE_API -d '{"name": "'$1'","access_token": "'$2'"}' > /dev/null
    fi
  fi
  git remote add $DST_TYPE git@$DST_TYPE.com:$DST_ACCOUNT/$1.git || echo "Remote already exists."
}

function update_repo
{
  echo -e "\033[31m(1/3)\033[0m" "Updating..."
  retry git pull -p
}

function import_repo
{
  echo -e "\033[31m(2/3)\033[0m" "Importing..."
  git remote set-head origin -d
  if [[ "$FORCE_UPDATE" == "true" ]]; then
    retry git push -f $DST_TYPE refs/remotes/origin/*:refs/heads/* --tags --prune
  else
    retry git push $DST_TYPE refs/remotes/origin/*:refs/heads/* --tags --prune
  fi
}

function _check_in_list () {
  local e match="$1"
  shift
  for e; do [[ "$e" == "$match" ]] && return 0; done
  return 1
}

function test_black_white_list
{
  WHITE_ARR=(`echo $WHITE_LIST | tr ',' ' '`)
  BLACK_ARR=(`echo $BLACK_LIST | tr ',' ' '`)
  _check_in_list $1 "${WHITE_ARR[@]}";in_white_list=$?
  _check_in_list $1 "${BLACK_ARR[@]}";in_back_list=$?
  
  if [[ $in_back_list -ne 0 ]] ; then
    if [[ -z $WHITE_LIST ]] || [[ $in_white_list -eq 0 ]] ; then
      return 0
    else
      echo "Skip, "$1" not in non-empty white list"$WHITE_LIST
      return 1
    fi
  else
    echo "Skip, "$1 "in black list: "$BLACK_LIST
    return 1
  fi
}

if [ ! -d "$CACHE_PATH" ]; then
  mkdir -p $CACHE_PATH
fi
cd $CACHE_PATH

all=0
success=0
skip=0
for repo in $SRC_REPOS
{
  all=$(($all + 1))
  if test_black_white_list $repo ; then
    echo -e "\n\033[31mBackup $repo ...\033[0m"

    cd $CACHE_PATH

    clone_repo $repo || delay_exit "clone and cd failed"  $repo || continue

    create_repo $repo $DST_TOKEN || delay_exit "create failed" $repo || continue

    update_repo || delay_exit "Update failed" $repo || continue

    import_repo && success=$(($success + 1)) || delay_exit "Push failed" $repo || continue
  else
    skip=$(($skip + 1))
  fi
}

failed=$(($all - $skip - $success))
echo "Total: $all, skip: $skip, successed: $success, failed: $failed."
echo "Failed: "$FAILED_LIST

if [[ "$DELAY_EXIT" == "true" ]]; then
  exit 1
fi
