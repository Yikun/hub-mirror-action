#!/bin/bash

DEBUG="${INPUT_DEBUG}"

if [[ "$DEBUG" == "true" ]]; then
  set -x
fi

mkdir -p /root/.ssh
echo "${INPUT_DST_KEY}" > /root/.ssh/id_rsa
chmod 600 /root/.ssh/id_rsa

pip3 install -r /hub-mirror/requirements.txt

python3 /hub-mirror/hubmirror.py --src "${INPUT_SRC}" --dst "${INPUT_DST}" \
--dst-token "${INPUT_DST_TOKEN}" \
--account-type "${INPUT_ACCOUNT_TYPE}" \
--clone-style "${INPUT_CLONE_STYLE}" \
--cache-path "${INPUT_CACHE_PATH}" \
--black-list "${INPUT_BLACK_LIST}" \
--white-list "${INPUT_WHITE_LIST}" \
--static-list "${INPUT_STATIC_LIST}" \
--force-update "${INPUT_FORCE_UPDATE}" \
--debug "${INPUT_DEBUG}" \
--timeout  "${INPUT_TIMEOUT}"

# Skip original code
exit $?
