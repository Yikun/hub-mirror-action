# Hub Mirror Action

简体中文 | [English](./README_en.md)

一个用于在hub间（例如Github，Gitee）账户代码仓库同步的action

## 用法

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

上面的配置完成了kunpencompute组织从github到gitee的同步，你可以在[测试和demo](https://github.com/Yikun/hub-mirror-action/tree/master/.github/workflows)找到完整用法。

## 谁在使用？
<a href="https://github.com/kunpengcompute/Kunpeng/blob/master/.github/workflows/gitee-repos-mirror.yml" > <img src="https://user-images.githubusercontent.com/1736354/95939597-040a1500-0e0f-11eb-99f8-4fc312751681.jpg" width="70"></a> <a href="https://github.com/openeuler-mirror/sync-config/blob/master/.github/workflows/repo-mirror.yml" > <img src="https://user-images.githubusercontent.com/1736354/95939584-feacca80-0e0e-11eb-88cf-bc002ded0bd5.jpg"  width="70"><a href="https://github.com/mindspore-ai/infrastructure/blob/master/.github/workflows/repos-mirror.yml" ><img src="https://user-images.githubusercontent.com/1736354/95939590-00768e00-0e0f-11eb-8436-7875a0bb6c92.jpg" width="70"></a> <a href="https://github.com/opengauss-mirror/sync-config/blob/master/.github/workflows/repo-mirror.yml" ><img src="https://user-images.githubusercontent.com/1736354/95939582-fc4a7080-0e0e-11eb-94e6-288c4afd0278.jpg"  width="70"></a> <a href="https://github.com/openlookeng/sync-config/blob/master/.github/workflows/repo-mirror.yml" ><img src="https://user-images.githubusercontent.com/1736354/95939601-05d3d880-0e0f-11eb-86a6-01ef95e7b85e.jpg"  width="70"></a><a href="https://github.com/WeBankFinTech/EventMesh/blob/master/.github/workflows/gitee-mirror.yml" ><img src="https://user-images.githubusercontent.com/1736354/95939579-fa80ad00-0e0e-11eb-9e44-264b1cf27374.jpg"  width="70"></a><a href="https://github.com/WeBankPartners/wecube-docs/blob/master/.github/workflows/sync-to-gitee.yml" ><img src="https://user-images.githubusercontent.com/1736354/95940763-c5c22500-0e11-11eb-9890-c7d1b6fa5aa3.jpg"  width="70"></a><a href="https://github.com/openbiox/UCSCXenaShiny/blob/master/.github/workflows/sync-gitee.yml" ><img src="https://user-images.githubusercontent.com/1736354/95940344-aaa2e580-0e10-11eb-863d-1ff2c5a04cfa.jpg"  width="70"></a><a href="https://github.com/renwu-cool/mirror-action/blob/master/.github/workflows/main.yml" ><img src="https://user-images.githubusercontent.com/1736354/95940437-eb9afa00-0e10-11eb-9fe2-65a8e68c6698.jpg"  width="70"></a><a href="https://github.com/search?q=hub-mirror-action&type=code"><img src="https://user-images.githubusercontent.com/1736354/95940571-42a0cf00-0e11-11eb-9ee2-cd497b50f06a.png"  width="70"></a>


## 参数详解
#### 必选参数
- `src` 需要被同步的源端账户名，如github/kunpengcompute，表示Github的kunpengcompute账户。
- `dst` 需要同步到的目的端账户名，如gitee/kunpengcompute，表示Gitee的kunpengcompute账户。
- `dst_key` 用于在目的端上传代码的私钥(默认可以从~/.ssh/id_rsa获取），可参考[生成/添加SSH公钥](https://gitee.com/help/articles/4181)或[generating SSH keys](https://docs.github.com/articles/generating-an-ssh-key/)生成，并确认对应公钥已经被正确配置在目的端。对应公钥，Github可以在[这里](https://github.com/settings/keys)配置，Gitee可以[这里](https://gitee.com/profile/sshkeys)配置。
- `dst_token` 创建仓库的API tokens， 用于自动创建不存在的仓库，Github可以在[这里](https://github.com/settings/tokens)找到，Gitee可以在[这里](https://gitee.com/profile/personal_access_tokens)找到。

#### 可选参数
- `account_type` 默认为user，源和目的的账户类型，可以设置为org（组织）或者user（用户），目前仅支持**同类型账户**（即组织到组织，或用户到用户）的同步。
- `clone_style` 默认为https，可以设置为ssh或者https。
- `cache_path` 默认为'', 将代码缓存在指定目录，用于与actions/cache配合以加速镜像过程。
- `black_list` 默认为'', 配置后，黑名单中的repos将不会被同步，如“repo1,repo2,repo3”。
- `white_list` 默认为'', 配置后，仅同步白名单中的repos，如“repo1,repo2,repo3”。
- `static_list` 默认为'', 配置后，仅同步静态列表，不会再动态获取需同步列表（黑白名单机制依旧生效），如“repo1,repo2,repo3”。
- `force_update` 默认为false, 配置后，启用git push -f强制同步，**注意：开启后，会强制覆盖目的端仓库**。
- `debug` 默认为false, 配置后，启用debug开关，会显示所有执行命令。

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

动态获取原端github/Yikun的repos，但仅同步名为hub-mirror-action，不同步hashes这个repo到Gittee

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

不会动态获取原端github/Yikun的repos，仅同步hub-mirror-action这个repo

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

## FAQ

- 如何在secrets添加dst_token和dst_key？
  下面是添加secrets的方法，也可以参考[secrets官方文档](https://help.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets)了解更多：
  1. **获取Token和Key**，分别获取[ssh key](https://gitee.com/profile/sshkeys)和[token](https://gitee.com/profile/personal_access_tokens)。
  2. **增加Secrets配置**，在配置仓库的Setting-Secrets中新增Secrets，例如GITEE_PRIVATE_KEY、GITEE_TOKEN
  3. **在Workflow中引用**， 可以用过类似`${{ secrets.GITEE_PRIVATE_KEY }}`来访问

## 参考
- [Hub mirror template](https://github.com/yi-Xu-0100/hub-mirror): 一个用于展示如何使用这个action的模板仓库. from @yi-Xu-0100
- [自动镜像 GitHub 仓库到 Gitee](https://github.com/ShixiangWang/sync2gitee): 一个关于如何使用这个action的介绍. from @ShixiangWang
- [巧用Github Action同步代码到Gitee](http://yikun.github.io/2020/01/17/%E5%B7%A7%E7%94%A8Github-Action%E5%90%8C%E6%AD%A5%E4%BB%A3%E7%A0%81%E5%88%B0Gitee/): Github Action第一篇软文

## 最后

如果觉得不错，**来个star**支持下作者吧！你的Star是我更新代码的动力！：）

想任何想吐槽或者建议的都可以直接飞个[issue](https://github.com/Yikun/hub-mirror-action/issues).

