# Hub Mirror Action

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
    dst_token:  ${{ secrets.GITEE_TOKEN }}
    account_type: org
```

你可以用上面的workflow完成**Github**的**kunpengcompute组织**下所有仓库到**Gitee**的同步。

你可以在[测试和demo](https://github.com/Yikun/hub-mirror-action/tree/master/.github/workflows)找到更多的使用方法。

## 参数详解

- `src` 需要被同步的源端账户名，如github/kunpengcompute，表示Github的kunpengcompute账户。
- `dst` 需要同步到的目的端账户名，如gitee/kunpengcompute，表示Gitee的kunpengcompute账户。
- `dst_key` 用于目的端上传代码的SSH key，用于上传代码，Github可以在[这里](https://gitee.com/profile/sshkeys)找到，Gitee可以[这里](https://github.com/settings/keys)找到
- `dst_token` 创建仓库的API tokens， 用于自动创建不存在的仓库，Github可以在[这里](https://github.com/settings/tokens)找到，Gitee可以在[这里](https://gitee.com/profile/personal_access_tokens)找到。
- `account_type` (optional) 默认为user，源和目的的账户类型，可以设置为org（组织）或者user（用户），目前仅支持**同类型账户**（即组织到组织，或用户到用户）的同步。
- `clone_style` (optional) 默认为https，可以设置为ssh或者https。
- `cache_path` (optional) 将代码缓存在指定目录，用于与actions/cache配合以加速镜像过程。
- `black_list` (optional) 配置后，黑名单中的repos将不会被同步，如“repo1,repo2,repo3”。
- `white_list` (optional) 配置后，仅同步白名单中的repos，如“repo1,repo2,repo3”。
- `static_list` (optional) 配置后，仅同步静态列表，不会再动态获取需同步列表（黑白名单机制依旧生效），如“repo1,repo2,repo3”。

## 举些例子

#### 组织同步，同步Github的kunpengcompute组织到Gitee
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

#### 白名单，仅同步Github的Yikun账户的hub-mirror-action这个repo到Gittee
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

#### 黑名单，同步除了hub-mirror-action和hashes之外的所有repos
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

#### clone方式，使用ssh方式进行clone
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

#### 指定目录cache
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

## FAQ

- 如何在secrets添加dst_token和dst_key？
  下面是添加secrets的方法，也可以参考[secrets官方文档](https://help.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets)了解更多：
  1. **获取Token和Key**，分别获取[ssh key](https://gitee.com/profile/sshkeys)和[token](https://gitee.com/profile/personal_access_tokens)。
  2. **增加Secrets配置**，在配置仓库的Setting-Secrets中新增Secrets，例如GITEE_PRIVATE_KEY、GITEE_TOKEN
  3. **在Workflow中引用**， 可以用过类似`${{ secrets.GITEE_PRIVATE_KEY }}`来访问
  
## 最后

喜欢的话点个Star哦，你的Star是我更新代码的动力！：）
