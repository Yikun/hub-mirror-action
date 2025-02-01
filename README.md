# Hub Mirror Action

简体中文 | [English](./README_en.md)

一个用于在hub间（例如Github，Gitee和Gitlab）账户代码仓库同步的action

## 用法

### 同步GitHub到Gitee
```yaml
steps:
- name: Mirror the Github organization repos to Gitee.
  uses: Yikun/hub-mirror-action@master
  with:
    # 支持Gitee, Github and Gitlab
    src: github/kunpengcompute
    # 支持Gitee, Github and Gitlab
    dst: gitee/kunpengcompute
    dst_key: ${{ secrets.GITEE_PRIVATE_KEY }}
    dst_token: ${{ secrets.GITEE_TOKEN }}
    # 支持Github/Gitee的用户、组织以及Gitlab的组
    account_type: org
    # 支持分别设置源和目的端的类型
    # src_account_type: org
    # dst_account_type: org
```

上面的配置完成了kunpencompute组织从github到gitee的同步，你可以在[测试和demo](https://github.com/Yikun/hub-mirror-action/tree/master/.github/workflows)找到完整用法。

有疑问、想法、问题、建议，可以通过[![Gitter](https://badges.gitter.im/hub-mirror-action/community.svg)](https://gitter.im/hub-mirror-action/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)找到我们。

## 谁在使用？
超过[100+](https://github.com/search?p=2&q=hub-mirror-action+%22account_type%22+%22org%22&type=Code)组织，[4000+](https://github.com/search?l=YAML&q=%22hub-mirror-action%22&type=Code)使用者正在使用，[50+](https://github.com/search?l=Markdown&q=%22hub-mirror-action%22&type=code)来自使用者的使用教程：

<img src="https://user-images.githubusercontent.com/1736354/130942306-7bfc32b7-ad2e-4117-b29d-17562c6536d6.jpg" width="90"></a><a href="https://github.com/openeuler-mirror/sync-config/blob/master/.github/workflows/repo-mirror.yml" > <img src="https://user-images.githubusercontent.com/1736354/130942376-279b5267-4842-41f0-b251-084acfd706a8.jpg"  width="90"></a><a href="https://github.com/Ascend/infrastructure/blob/master/.github/workflows/repo-mirror.yml" > <img src="https://user-images.githubusercontent.com/1736354/130942173-afd2ad34-3ba1-4a6e-b0eb-b72050239c46.jpg" width="90"></a><a href="https://github.com/mindspore-ai/infrastructure/blob/master/.github/workflows/repos-mirror.yml" ><img src="https://user-images.githubusercontent.com/1736354/130942787-b01f79a9-c115-46fd-a2b0-23e5f84cba61.jpg" width="90"></a> <a href="https://github.com/opengauss-mirror/sync-config/blob/master/.github/workflows/repo-mirror.yml" ><img src="https://user-images.githubusercontent.com/1736354/130942900-f8ff41bb-a827-425c-a132-569ba78ed18c.jpg"  width="90"></a> <a href="https://github.com/openlookeng/sync-config/blob/master/.github/workflows/repo-mirror.yml" ><img src="https://user-images.githubusercontent.com/1736354/130942988-c32b0224-ecc2-454a-b5e8-376ae25c092d.jpg"  width="90"></a><a href="https://github.com/openharmony" > <img src="https://user-images.githubusercontent.com/1736354/130943738-6a8fb234-7829-4b70-a8a7-1716fda2c5b5.jpg" width="90"></a><a href="https://github.com/EdgeGallery/sync-gitee-repo/blob/master/.github/workflows/gitee-repo-mirror.yml" > <img src="https://user-images.githubusercontent.com/1736354/130944072-b4eb2ca2-ab15-456f-946b-043c114dc783.jpg" width="90"></a><a href="https://github.com/kunpengcompute/Kunpeng/blob/master/.github/workflows/gitee-repos-mirror.yml" > <a href="https://github.com/WeBankFinTech/fes.js/blob/master/.github/workflows/gitee-mirror.yml" ><img src="https://user-images.githubusercontent.com/1736354/130943240-f08ba34f-7971-4e17-8ee2-35b8718aba28.jpg"  width="90"></a><a href="https://github.com/openbiox/UCSCXenaShiny/blob/master/.github/workflows/sync-gitee.yml" ><img src="https://user-images.githubusercontent.com/1736354/95940344-aaa2e580-0e10-11eb-863d-1ff2c5a04cfa.jpg"  width="90"></a><a href="https://github.com/renwu-cool/mirror-action/blob/master/.github/workflows/main.yml" ><img src="https://user-images.githubusercontent.com/1736354/95940437-eb9afa00-0e10-11eb-9fe2-65a8e68c6698.jpg"  width="90"></a><a href="https://github.com/kubesphere/website/blob/c7ebf051d2b7d712b88cccf5424fae0cef6c1c82/.github/workflows/build.yml"><img src="https://user-images.githubusercontent.com/1736354/131271726-5f5e1f75-2e84-40d6-99ac-0bceaca41b2a.jpg"  width="90"></a> <a href="https://github.com/go-atomci/atomci/blob/master/.github/workflows/sync-to-gitee.yml"><img src="https://user-images.githubusercontent.com/1736354/147518496-d92da9f1-24ed-4fde-b170-5559aa0512ff.png"  width="90"></a> <a href="https://github.com/RapidAI/.github/blob/main/.github/workflows/SyncToGitee.yml"><img src="https://user-images.githubusercontent.com/28639377/226772424-1a926e15-f418-4371-8750-c0826ef92cd8.png"  width="90"></a> <a href="https://github.com/LingmoOS/lingmo-repo-sync"><img src="https://github.com/user-attachments/assets/9eddf2ae-3b23-467f-bed8-9582d896cb4d"  width="90"></a> <a href="https://github.com/search?q=hub-mirror-action&type=code"><img src="https://user-images.githubusercontent.com/1736354/95940571-42a0cf00-0e11-11eb-9ee2-cd497b50f06a.png"  width="90"></a>


## 参数详解
#### 必选参数
- `src` 需要被同步的源端账户名，如github/kunpengcompute，表示Github的kunpengcompute账户。
- `dst` 需要同步到的目的端账户名，如gitee/kunpengcompute，表示Gitee的kunpengcompute账户。
- `dst_key` 用于在目的端上传代码的私钥(默认可以从~/.ssh/id_rsa获取），可参考[生成/添加SSH公钥](https://gitee.com/help/articles/4181)或[generating SSH keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)生成，并确认对应公钥已经被正确配置在目的端。对应公钥，Github可以在[这里](https://github.com/settings/keys)配置，Gitee可以[这里](https://gitee.com/profile/sshkeys)配置，Gitlab可以在[这里](https://gitlab.com/-/user_settings/ssh_keys)配置。
- `dst_token` 创建仓库的API tokens， 用于自动创建不存在的仓库，Github可以在[这里](https://github.com/settings/tokens)找到，Gitee可以在[这里](https://gitee.com/profile/personal_access_tokens)找到，Gitlab可以在[这里](https://gitlab.com/-/user_settings/personal_access_tokens)找到（Required scopes: api, read_api, read_repository, write_repository）。

#### 可选参数
- `account_type` 默认为user，源和目的的账户类型，可以设置为org（组织）、user（用户）或者group（组），该参数支持**同类型账户**（即组织到组织，或用户到用户，或组到组）的同步。如果源目的仓库是不同类型，请单独使用`src_account_type`和`dst_account_type`配置。
- `src_account_type` 默认为`account_type`，源账户类型，可以设置为org（组织）、user（用户）或者group（组）。
- `dst_account_type` 默认为`account_type`，目的账户类型，可以设置为org（组织）、user（用户）或者group（组）。
- `clone_style` 默认为https，可以设置为ssh或者https。当设置为ssh时，你需要将`dst_key`所对应的公钥同时配置到源端和目的端。
- `cache_path` 默认为'', 将代码缓存在指定目录，用于与actions/cache配合以加速镜像过程。
- `black_list` 默认为'', 配置后，黑名单中的repos将不会被同步，如“repo1,repo2,repo3”。
- `white_list` 默认为'', 配置后，仅同步白名单中的repos，如“repo1,repo2,repo3”。
- `static_list` 默认为'', 配置后，仅同步静态列表，不会再动态获取需同步列表（黑白名单机制依旧生效），如“repo1,repo2,repo3”。
- `force_update` 默认为false, 配置后，启用git push -f强制同步，**注意：开启后，会强制覆盖目的端仓库**。
- `debug` 默认为false, 配置后，启用debug开关，会显示所有执行命令。
- `timeout` 默认为'30m', 用于设置每个git命令的超时时间，'600'=>600s, '30m'=>30 mins, '1h'=>1 hours
- `mappings` 源仓库映射规则，比如'A=>B, C=>CC', A会被映射为B，C会映射为CC，映射不具有传递性。主要用于源和目的仓库名不同的镜像。
- `lfs` 提供[git lfs](https://git-lfs.com/)支持, 默认为false, 配置为true后，调用`git lfs fetch --all`和`git lfs push --all`进行同步。
- `api_timeout`（可选）默认值为 `60`，用于设置 API 请求的超时时间（单位：秒）。
  例如：`api_timeout: '90'`

## 举些例子

#### 组织同步

同步Github的kunpengcompute组织到Gitee

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

#### 黑/白名单

动态获取源端github/Yikun的repos，但仅同步名为hub-mirror-action，不同步hashes这个repo到Gitee

```yaml
- name: Single repo mirror
  uses: Yikun/hub-mirror-action@master
  with:
    src: github/Yikun
    dst: gitee/yikunkero
    dst_key: ${{ secrets.GITEE_PRIVATE_KEY }}
    dst_token: ${{ secrets.GITEE_TOKEN }}
    white_list: "hub-mirror-action"
    black_list: "hashes"
```

#### 静态名单（可用于单一仓库同步）

不会动态获取源端github/Yikun的repos，仅同步hub-mirror-action这个repo

```yaml
- name: Black list
  uses: Yikun/hub-mirror-action@master
  with:
    src: github/Yikun
    dst: gitee/yikunkero
    dst_key: ${{ secrets.GITEE_PRIVATE_KEY }}
    dst_token: ${{ secrets.GITEE_TOKEN }}
    static_list: "hub-mirror-action"
```

#### clone方式

使用ssh方式进行clone

说明：请把`dst_key`所的公钥配置到源端（在这里为github）及目的端（在这里为gitee）

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

#### 指定目录cache
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

#### 强制更新，并打开debug日志开关
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

#### 设置命令行超时时间为1小时
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

#### 仓库名不同时同步（github/yikun/yikun.github.com to gitee/yikunkero/blog）
```yaml
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

#### 仅同步非fork且非private的仓库
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

#### 支持LFS同步
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

#### 同步GitHub到Gitlab
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

## FAQ

- 如何在secrets添加dst_token和dst_key？
  下面是添加secrets的方法，也可以参考[secrets官方文档](https://help.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets)了解更多：
  1. **获取Token和Key**，例如
  - Github: 配置并保存[ssh key](https://github.com/settings/keys)和[token](https://github.com/settings/tokens)
  - Gitee: 配置并保存[ssh key](https://gitee.com/profile/sshkeys)和[token](https://gitee.com/profile/personal_access_tokens)
  - Gtilab: 配置并保存[ssh key](https://gitlab.com/-/user/settings/keys)和[token](https://gitlab.com/-/user_settings/personal_access_tokens)
  2. **增加Secrets配置**，在配置仓库的Setting-Secrets中新增Secrets，例如`GITEE_PRIVATE_KEY`\`GITLAB_PRIVATE_KEY`、`GITEE_TOKEN`\`GITLAB_TOKEN`。
  3. **在Workflow中引用**， 可以用过类似`${{ secrets.GITEE_PRIVATE_KEY }}`来访问。

## 参考
- [Hub mirror template](https://github.com/yi-Xu-0100/hub-mirror): 一个用于展示如何使用这个action的模板仓库. from @yi-Xu-0100
- [自动镜像 GitHub 仓库到 Gitee](https://github.com/ShixiangWang/sync2gitee): 一个关于如何使用这个action的介绍. from @ShixiangWang
- [巧用Github Action同步代码到Gitee](http://yikun.github.io/2020/01/17/%E5%B7%A7%E7%94%A8Github-Action%E5%90%8C%E6%AD%A5%E4%BB%A3%E7%A0%81%E5%88%B0Gitee/): Github Action第一篇软文

## 最后

如果觉得不错，**来个star**支持下作者吧！你的Star是我更新代码的动力！：）

想任何想吐槽或者建议的都可以直接飞个[issue](https://github.com/Yikun/hub-mirror-action/issues).

