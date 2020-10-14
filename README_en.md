# Hub Mirror Action

English | [简体中文](./README.md)

Action for mirroring repos between Hubs (like Github and Gitee)

## Tutorial

```yaml
steps:
- name: Mirror the Github organization repos to Gitee.
  uses: Yikun/hub-mirror-action@master
  with:
    src: github/kunpengcompute
    dst: gitee/kunpengcompute
    dst_key: ${{ secrets.GITEE_PRIVATE_KEY }}
    dst_token: ${{ secrets.GITEE_TOKEN }}
    account_type: org
```

Here is a workflow to mirror the kunpengcompute org repos from Github to Gitee, see more complete workflows in [here](https://github.com/Yikun/hub-mirror-action/tree/master/.github/workflows).

## Who are using?
<a href="https://github.com/kunpengcompute/Kunpeng/blob/master/.github/workflows/gitee-repos-mirror.yml" > <img src="https://user-images.githubusercontent.com/1736354/95939597-040a1500-0e0f-11eb-99f8-4fc312751681.jpg" width="70"></a> <a href="https://github.com/openeuler-mirror/sync-config/blob/master/.github/workflows/repo-mirror.yml" > <img src="https://user-images.githubusercontent.com/1736354/95939584-feacca80-0e0e-11eb-88cf-bc002ded0bd5.jpg"  width="70"><a href="https://github.com/mindspore-ai/infrastructure/blob/master/.github/workflows/repos-mirror.yml" ><img src="https://user-images.githubusercontent.com/1736354/95939590-00768e00-0e0f-11eb-8436-7875a0bb6c92.jpg" width="70"></a> <a href="https://github.com/opengauss-mirror/sync-config/blob/master/.github/workflows/repo-mirror.yml" ><img src="https://user-images.githubusercontent.com/1736354/95939582-fc4a7080-0e0e-11eb-94e6-288c4afd0278.jpg"  width="70"></a> <a href="https://github.com/openlookeng/sync-config/blob/master/.github/workflows/repo-mirror.yml" ><img src="https://user-images.githubusercontent.com/1736354/95939601-05d3d880-0e0f-11eb-86a6-01ef95e7b85e.jpg"  width="70"></a><a href="https://github.com/WeBankFinTech/EventMesh/blob/master/.github/workflows/gitee-mirror.yml" ><img src="https://user-images.githubusercontent.com/1736354/95939579-fa80ad00-0e0e-11eb-9e44-264b1cf27374.jpg"  width="70"></a><a href="https://github.com/WeBankPartners/wecube-docs/blob/master/.github/workflows/sync-to-gitee.yml" ><img src="https://user-images.githubusercontent.com/1736354/95940763-c5c22500-0e11-11eb-9890-c7d1b6fa5aa3.jpg"  width="70"></a><a href="https://github.com/openbiox/UCSCXenaShiny/blob/master/.github/workflows/sync-gitee.yml" ><img src="https://user-images.githubusercontent.com/1736354/95940344-aaa2e580-0e10-11eb-863d-1ff2c5a04cfa.jpg"  width="70"></a><a href="https://github.com/renwu-cool/mirror-action/blob/master/.github/workflows/main.yml" ><img src="https://user-images.githubusercontent.com/1736354/95940437-eb9afa00-0e10-11eb-9fe2-65a8e68c6698.jpg"  width="70"></a><a href="https://github.com/search?q=hub-mirror-action&type=code"><img src="https://user-images.githubusercontent.com/1736354/95940571-42a0cf00-0e11-11eb-9ee2-cd497b50f06a.png"  width="70"></a>

## Usage

#### Required
- `src` source account, such as `github/kunpengcompute`, is the Github kunpengcompute account.
- `dst` Destination account, such as `/kunpengcompute`, is the Gitee kunpengcompute account.
- `dst_key` the private key to push code in destination account (default in ~/.ssh/id_rsa), you can see [generating SSH keys](https://docs.github.com/articles/generating-an-ssh-key/) to generate the pri/pub key, and make sure the pub key has been added in destination. You can set Github ssh key in [here](https://github.com/settings/keys)，set the Gitee ssh key in [here](https://gitee.com/profile/sshkeys).
- `dst_token` the API token to create non-existent repo, You can get Github token in [here](https://github.com/settings/tokens), and the Gitee in [here](https://gitee.com/profile/personal_access_tokens).

#### Optional
- `account_type` (optional) default is `user`, the account type of src and dst account, can be set to `org` or `user`，only support mirror between same account type (that is "org to org" or "user to user").
- `clone_style` (optional) default is `https`, can be set to `ssh` or `https`.
- `cache_path` (optional) let code clone in specific path, can be used with actions/cache to speed up mirror.
- `black_list` (optional) the black list, such as “repo1,repo2,repo3”.
- `white_list` (optional) the white list, such as “repo1,repo2,repo3”.
- `static_list` (optional) Only mirror repos in the static list, but don't get list from repo api dynamically (the white/black list is still available). like 'repo1,repo2,repo3'
- `force_update` (optional) Force to update the destination repo, use '-f' flag do 'git push'

## Scenarios

#### Organization mirror, mirror the Github/kunpengcompute to Gitee/kunpengcompute
```yaml
- name: Organization mirror
  uses: Yikun/hub-mirror-action@master
  with:
    src: github/kunpengcompute
    dst: gitee/kunpengcompute
    dst_key: ${{ secrets.GITEE_PRIVATE_KEY }}
    dst_token: ${{ secrets.GITEE_TOKEN }}
    account_type: org
```

#### White/Black list, only mirror the Yikun/hub-mirror-action but not Yikun/hashes
```yaml
- name: Single repo mirror
  uses: Yikun/hub-mirror-action@master
  with:
    src: github/Yikun
    dst: gitee/yikunkero
    dst_key: ${{ secrets.GITEE_PRIVATE_KEY }}
    dst_token: ${{ secrets.GITEE_TOKEN }}
    white_list: "hub-mirror-action"
    white_list: "hashes"
```

#### Static list, only mirror the repos `hub-mirror-action` and `hashes`
```yaml
- name: Black list
  uses: Yikun/hub-mirror-action@master
  with:
    src: github/Yikun
    dst: gitee/yikunkero
    dst_key: ${{ secrets.GITEE_PRIVATE_KEY }}
    dst_token: ${{ secrets.GITEE_TOKEN }}
    static_list: "hub-mirror-action,hashes"
```

#### clone style, use `ssh` clone style
```yaml
- name: ssh clone style
  uses: Yikun/hub-mirror-action@master
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
  uses: Yikun/hub-mirror-action@master
  with:
    src: github/Yikun
    dst: gitee/yikunkero
    dst_key: ${{ secrets.GITEE_PRIVATE_KEY }}
    dst_token: ${{ secrets.GITEE_TOKEN }}
    cache_path: /github/workspace/hub-mirror-cache
```

#### Force udpate and enable the debug flag
```yaml
- name: Mirror with force push (git push -f)
  uses: Yikun/hub-mirror-action@master
  with:
    src: github/Yikun
    dst: gitee/yikunkero
    dst_key: ${{ secrets.GITEE_PRIVATE_KEY }}
    dst_token: ${{ secrets.GITEE_TOKEN }}
    force_update: true
    debug: true
```

## FAQ
- How to use `secrets` to add token and key?
  
  You can use below steps to add secrets, you can also see more in [Secrets](https://help.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets).

  1. **Get Token and Key**，you can get them in [ssh key](https://gitee.com/profile/sshkeys) and [token](https://gitee.com/profile/personal_access_tokens).
  2. **Add Secrets**，add settings-secrets in repo，like `GITEE_PRIVATE_KEY`、`GITEE_TOKEN`
  3. **Add workflow**，add the workflow file into .github/workflows.

## Reference
- [Hub mirror template](https://github.com/yi-Xu-0100/hub-mirror): A template repo to show how to use this action. from @yi-Xu-0100
- [Auto-Sync GitHub Repositories to Gitee](https://github.com/ShixiangWang/sync2gitee): An introduction about how to use this action. from @ShixiangWang
- [Use Github Action to sync reois to Gitee](http://yikun.github.io/2020/01/17/%E5%B7%A7%E7%94%A8Github-Action%E5%90%8C%E6%AD%A5%E4%BB%A3%E7%A0%81%E5%88%B0Gitee/): The blog for this action.
