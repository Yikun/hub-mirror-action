# Hub Mirror Action

English | [简体中文](./README.md)

Action for mirroring repos between Hubs (like GitHub, Gitee, and GitLab).

## Tutorial

```yaml
steps:
- name: Mirror the Github organization repos to Gitee.
  uses: Yikun/hub-mirror-action@master
  with:
    # Support gitee, github and gitlab
    src: github/kunpengcompute
    # Support gitee, github and gitlab
    dst: gitee/kunpengcompute
    dst_key: ${{ secrets.GITEE_PRIVATE_KEY }}
    dst_token: ${{ secrets.GITEE_TOKEN }}
    # Support github/gitee user, org and gitlab group
    account_type: org
    # Supporte set account type speparately
    # src_account_type: org
    # dst_account_type: org
```

Here is a workflow to mirror the kunpengcompute org repos from Github to Gitee, see more complete workflows in [here](https://github.com/Yikun/hub-mirror-action/tree/master/.github/workflows).

Please refer to [scenarios](https://github.com/Yikun/hub-mirror-action/blob/master/README_en.md#scenarios) for more examples.

## Who are using?
More than [100+](https://github.com/search?p=2&q=hub-mirror-action+%22account_type%22+%22org%22&type=Code) organizations，[4000+](https://github.com/search?l=YAML&q=%22hub-mirror-action%22&type=Code) users are using, [50+](https://github.com/search?l=Markdown&q=%22hub-mirror-action%22&type=code) related blogs from users：

<img src="https://user-images.githubusercontent.com/1736354/130942306-7bfc32b7-ad2e-4117-b29d-17562c6536d6.jpg" width="90"></a><a href="https://github.com/openeuler-mirror/sync-config/blob/master/.github/workflows/repo-mirror.yml" > <img src="https://user-images.githubusercontent.com/1736354/130942376-279b5267-4842-41f0-b251-084acfd706a8.jpg"  width="90"></a><a href="https://github.com/Ascend/infrastructure/blob/master/.github/workflows/repo-mirror.yml" > <img src="https://user-images.githubusercontent.com/1736354/130942173-afd2ad34-3ba1-4a6e-b0eb-b72050239c46.jpg" width="90"></a><a href="https://github.com/mindspore-ai/infrastructure/blob/master/.github/workflows/repos-mirror.yml" ><img src="https://user-images.githubusercontent.com/1736354/130942787-b01f79a9-c115-46fd-a2b0-23e5f84cba61.jpg" width="90"></a> <a href="https://github.com/opengauss-mirror/sync-config/blob/master/.github/workflows/repo-mirror.yml" ><img src="https://user-images.githubusercontent.com/1736354/130942900-f8ff41bb-a827-425c-a132-569ba78ed18c.jpg"  width="90"></a> <a href="https://github.com/openlookeng/sync-config/blob/master/.github/workflows/repo-mirror.yml" ><img src="https://user-images.githubusercontent.com/1736354/130942988-c32b0224-ecc2-454a-b5e8-376ae25c092d.jpg"  width="90"></a><a href="https://github.com/openharmony" > <img src="https://user-images.githubusercontent.com/1736354/130943738-6a8fb234-7829-4b70-a8a7-1716fda2c5b5.jpg" width="90"></a><a href="https://github.com/EdgeGallery/sync-gitee-repo/blob/master/.github/workflows/gitee-repo-mirror.yml" > <img src="https://user-images.githubusercontent.com/1736354/130944072-b4eb2ca2-ab15-456f-946b-043c114dc783.jpg" width="90"></a><a href="https://github.com/kunpengcompute/Kunpeng/blob/master/.github/workflows/gitee-repos-mirror.yml" > <a href="https://github.com/WeBankFinTech/fes.js/blob/master/.github/workflows/gitee-mirror.yml" ><img src="https://user-images.githubusercontent.com/1736354/130943240-f08ba34f-7971-4e17-8ee2-35b8718aba28.jpg"  width="90"></a><a href="https://github.com/openbiox/UCSCXenaShiny/blob/master/.github/workflows/sync-gitee.yml" ><img src="https://user-images.githubusercontent.com/1736354/95940344-aaa2e580-0e10-11eb-863d-1ff2c5a04cfa.jpg"  width="90"></a><a href="https://github.com/renwu-cool/mirror-action/blob/master/.github/workflows/main.yml" ><img src="https://user-images.githubusercontent.com/1736354/95940437-eb9afa00-0e10-11eb-9fe2-65a8e68c6698.jpg"  width="90"></a><a href="https://github.com/kubesphere/website/blob/c7ebf051d2b7d712b88cccf5424fae0cef6c1c82/.github/workflows/build.yml"><img src="https://user-images.githubusercontent.com/1736354/131271726-5f5e1f75-2e84-40d6-99ac-0bceaca41b2a.jpg"  width="90"></a> <a href="https://github.com/go-atomci/atomci/blob/master/.github/workflows/sync-to-gitee.yml"><img src="https://user-images.githubusercontent.com/1736354/147518496-d92da9f1-24ed-4fde-b170-5559aa0512ff.png"  width="90"></a> <a href="https://github.com/RapidAI/.github/blob/main/.github/workflows/SyncToGitee.yml"><img src="https://user-images.githubusercontent.com/28639377/226772424-1a926e15-f418-4371-8750-c0826ef92cd8.png"  width="90"></a><a href="https://github.com/LingmoOS/lingmo-repo-sync"><img src="https://github.com/user-attachments/assets/9eddf2ae-3b23-467f-bed8-9582d896cb4d"  width="90"></a> <a href="https://github.com/search?q=hub-mirror-action&type=code"><img src="https://user-images.githubusercontent.com/1736354/95940571-42a0cf00-0e11-11eb-9ee2-cd497b50f06a.png"  width="90"></a>

## Usage

#### Required
- `src` source account, such as `github/kunpengcompute`, is the Github kunpengcompute account.
- `dst` Destination account, such as `/kunpengcompute`, is the Gitee kunpengcompute account.
- `dst_key` the private key to push code in destination account (default in ~/.ssh/id_rsa), you can see [generating SSH keys](https://docs.github.com/articles/generating-an-ssh-key/) to generate the pri/pub key, and make sure the pub key has been added in destination. You can set Github ssh key in [here](https://github.com/settings/keys)，set the Gitee ssh key in [here](https://gitee.com/profile/sshkeys) set the Gitlab ssh key in [here](https://gitlab.com/-/user_settings/ssh_keys).
- `dst_token` the API token to create non-existent repo, You can get Github token in [here](https://github.com/settings/tokens), and the Gitee in [here](https://gitee.com/profile/personal_access_tokens). and for GitLab in [here](https://gitlab.com/-/user_settings/personal_access_tokens) (Required scopes: api, read_api, read_repository, write_repository).

#### Optional
- `account_type` (optional) default is `user`, the account type of src and dst account, can be set to `org` or `user`，For GitLab: can be set to `group` or `user`,only support mirror between same account type (that is "org to org" or "user to user" or "group to group"). if u wanna mirror difference account type, use the `src_account_type` and `dst_account_type` please.
- `src_account_type` (optional) default is `account_type`, the account type of src account, can be set to `org` or `user` or `group`.
- `dst_account_type` (optional) default is `account_type`, the account type of dst account, can be set to `org` or `user`r `group`.
- `clone_style` (optional) default is `https`, can be set to `ssh` or `https`.When you are using ssh clone style, you need to configure the public key of `dst_key` to both source end and destination end.
- `cache_path` (optional) let code clone in specific path, can be used with actions/cache to speed up mirror.
- `black_list` (optional) the black list, such as “repo1,repo2,repo3”.
- `white_list` (optional) the white list, such as “repo1,repo2,repo3”.
- `static_list` (optional) Only mirror repos in the static list, but don't get list from repo api dynamically (the white/black list is still available). like 'repo1,repo2,repo3'
- `force_update` (optional) Force to update the destination repo, use '-f' flag do 'git push'
- `timeout` (optional) Default is '30m', set the timeout for every git command, like '600'=>600s, '30m'=>30 mins, '1h'=>1 hours
- `mappings` (optional) Default is empty, the source repos mappings, such as 'A=>B, C=>CC', source repo name would be mapped follow the rule: A to B, C to CC. Mapping is not transitive.
- `lfs` (optional) Default is false, support [git lfs](https://git-lfs.com/), call `git lfs fetch --all` and `git lfs push --all` to support lfs mirror.
- `api_timeout` (optional) Default is `60`, sets the timeout for API requests (in seconds). 
  Example usage: `api_timeout: '90'`

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
#### GitLab group mirror, mirror from GitHub organization to GitLab group
```yaml
- name: GitLab group mirror
  uses: Yikun/hub-mirror-action@master
  with:
    src: github/organization-name
    dst: gitlab/group-name
    dst_key: ${{ secrets.GITLAB_PRIVATE_KEY }}
    dst_token: ${{ secrets.GITLAB_TOKEN }}
    account_type: group
    src_account_type: org
    dst_account_type: group
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
Note: please configure the public key of `dst_key` to the source (github in here) and destination(gitee in here)

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

#### Set command timeout to an hour
```yaml
- name: Mirror with force push (git push -f)
  uses: Yikun/hub-mirror-action@master
  with:
    src: github/Yikun
    dst: gitee/yikunkero
    dst_key: ${{ secrets.GITEE_PRIVATE_KEY }}
    dst_token: ${{ secrets.GITEE_TOKEN }}
    force_update: true
    timeout: '1h'
```

#### Sync between different repo name（github/yikun/yikun.github.com to gitee/yikunkero/blog）
```
- name: mirror with mappings
  uses: Yikun/hub-mirror-action@mappings
  with:
    src: github/yikun
    dst: gitee/yikunkero
    dst_key: ${{ secrets.GITEE_PRIVATE_KEY }}
    dst_token: ${{ secrets.GITEE_TOKEN }}
    mappings: "yikun.github.com=>blog"
    static_list: "yikun.github.com"
```

### Only sync repository list exclude private and fork
```yaml
- name: Get repository list exclude private and fork
  id: repo
  uses: yi-Xu-0100/repo-list-generator@v1.0.1
- name: Mirror repository list exclude private and fork
  uses: Yikun/hub-mirror-action@master
  with:
    src: github/Yikun
    dst: gitee/yikunkero
    dst_key: ${{ secrets.GITEE_PRIVATE_KEY }}
    dst_token: ${{ secrets.GITEE_TOKEN }}
    static_list: ${{ steps.repo.outputs.repoList }}
```

#### Support LFS mirror
```yaml
- name: Mirror with lfs (git lfs fetch/push --all)
  uses: Yikun/hub-mirror-action@master
  with:
    src: github/Yikun
    dst: gitee/yikunkero
    dst_key: ${{ secrets.GITEE_PRIVATE_KEY }}
    dst_token: ${{ secrets.GITEE_TOKEN }}
    lfs: true
```

## FAQ
- How to use `secrets` to add token and key?

  You can use below steps to add secrets, you can also see more in [Secrets](https://help.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets).

  1. **Get Token and Key**:
  - Github: Configure and save your [ssh key](https://github.com/settings/keys)和[token](https://github.com/settings/tokens)
  - Gitee: Configure and save your [ssh key](https://gitee.com/profile/sshkeys)和[token](https://gitee.com/profile/personal_access_tokens)
  - Gtilab: Configure and save your [ssh key](https://gitlab.com/-/user/settings/keys)和[token](https://gitlab.com/-/user_settings/personal_access_tokens)
  2. **Add Secrets**，add settings-secrets in repo，like `GITEE_PRIVATE_KEY`、`GITEE_TOKEN` or `GITLAB_PRIVATE_KEY`、`GITLAB_TOKEN`
  3. **Add workflow**，add the workflow file into .github/workflows.

## Reference
- [Hub mirror template](https://github.com/yi-Xu-0100/hub-mirror): A template repo to show how to use this action. from @yi-Xu-0100
- [Auto-Sync GitHub Repositories to Gitee](https://github.com/ShixiangWang/sync2gitee): An introduction about how to use this action. from @ShixiangWang
- [Use Github Action to sync reois to Gitee](http://yikun.github.io/2020/01/17/%E5%B7%A7%E7%94%A8Github-Action%E5%90%8C%E6%AD%A5%E4%BB%A3%E7%A0%81%E5%88%B0Gitee/): The blog for this action.

## Platform-Specific Notes

### GitLab
- Uses `group` instead of `org` for organizational accounts
- Only top-level groups are supported for mirroring. Nested subgroups (group/subgroup) are not supported yet
- Requires API token with appropriate scopes (api, read_api, read_repository, write_repository)
- When mirroring to GitLab, ensure your group/user has sufficient permissions to create repositories
- GitLab.com has API rate limits of 2000 requests per minute for authenticated users
- [GitLab API Documentation](https://docs.gitlab.com/ee/api/): Official GitLab API documentation
- [GitLab Personal Access Tokens](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html): Guide for creating GitLab tokens