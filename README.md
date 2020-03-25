## Hub Mirror Action

English | [简体中文](./README_CN.md)

Action for mirroring repos between Hubs (like Github and Gitee)

### Tutorial

Here is a complete organization mirror workflows:

```yaml
steps:
- name: Mirror the Github organization repos to Gitee.
  uses: Yikun/hub-mirror-action@master
  with:
    src: github/kunpengcompute
    dst: gitee/kunpengcompute
    dst_key: ${{ secrets.GITEE_PRIVATE_KEY }}
    dst_token:  ${{ secrets.GITEE_TOKEN }}
    account_type: org
```
You can use below steps to add secrets, you can also see more in [Secrets]((https://help.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets)) 

1. **Get Token and Key**，you can get them in [ssh key](https://gitee.com/profile/sshkeys) and [token](https://gitee.com/profile/personal_access_tokens).
2. **Add Secrets**，add settings-secrets in repo，like `GITEE_PRIVATE_KEY`、`GITEE_TOKEN`
3. **Add workflow**，add the workflow file into .github/workflows.

After above steps，You have add a workflow to mirro all repos from **Github/kunpengcompute organization** to **Gitee/kunpengcompute organization**.

You can see more usage workflow in [demos](https://github.com/Yikun/hub-mirror-action/tree/master/.github/workflows).

### Usage

- `src` source account, such as `github/kunpengcompute`, is the Github kunpengcompute account.
- `dst` Destination account, such as `/kunpengcompute`, is the Gitee kunpengcompute account.
- `dst_key` the ssh key to push code in destination account,You can get the Github sshkeys in [here](https://gitee.com/profile/sshkeys)，the Gitee ssh key in [here](https://github.com/settings/keys).
- `dst_token` the API token to create non-existent repo, You can get Github token in [here](https://github.com/settings/tokens), and the Gitee in [here](https://gitee.com/profile/personal_access_tokens).
- `account_type` (optional) default is `user`, the account type of src and dst account, can be set to `org` or `user`，only support mirror between same account type (that is "org to org" or "user to user").
- `clone_style` (optional) default is `https`, can be set to `ssh` or `https`.
- `cache_path` (optional) let code clone in specific path, can be used with actions/cache to speed up mirror.
- `black_list` (optional) the black list, such as “repo1,repo2,repo3”.
- `white_list` (optional) the white list, such as “repo1,repo2,repo3”.

### Scenarios

#### Organization mirror, mirror the Github/kunpengcompute to Gitee/kunpengcompute
```yaml
- name: Organization mirror
  uses: Yikun/hub-mirror-action
  with:
    src: github/kunpengcompute
    dst: gitee/kunpengcompute
    dst_key: ${{ secrets.GITEE_PRIVATE_KEY }}
    dst_token: ${{ secrets.GITEE_TOKEN }}
    account_type: org
```

#### White list, only mirror the Yikun/hub-mirror-action
```yaml
- name: Single repo mirror
  uses: Yikun/hub-mirror-action
  with:
    src: github/Yikun
    dst: gitee/yikunkero
    dst_key: ${{ secrets.GITEE_PRIVATE_KEY }}
    dst_token: ${{ secrets.GITEE_TOKEN }}
    white_list: "hub-mirror-action"
```

#### Black list, only mirror the repos excepts `hub-mirror-action` and `hashes`
```yaml
- name: Black list
  uses: Yikun/hub-mirror-action
  with:
    src: github/Yikun
    dst: gitee/yikunkero
    dst_key: ${{ secrets.GITEE_PRIVATE_KEY }}
    dst_token: ${{ secrets.GITEE_TOKEN }}
    white_list: "hub-mirror-action,hashes"
```

#### clone style, use `ssh` clone style
```yaml
- name: ssh clone style
  uses: Yikun/hub-mirror-action
  with:
    src: github/Yikun
    dst: gitee/yikunkero
    dst_key: ${{ secrets.GITEE_PRIVATE_KEY }}
    dst_token: ${{ secrets.GITEE_TOKEN }}
    clone_style: "ssh"
```

#### set sepecific cache
```yaml
- name: Mirror with specific cache
  uses: Yikun/hub-mirror-action
  with:
    src: github/Yikun
    dst: gitee/yikunkero
    dst_key: ${{ secrets.GITEE_PRIVATE_KEY }}
    dst_token: ${{ secrets.GITEE_TOKEN }}
    cache_path: /github/workspace/hub-mirror-cache
```
