## Hub Mirror Action

一个用于在hub间（例如Github，Gitee）账户代码仓库同步的action

### 用法

一个完整的组织仓库同步的配置可以参考：

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
上面的配置执行后，将完成**Github**的**kunpengcompute****组织**下所有仓库到**Gitee**的同步。

You could take a look on the [verify workflow](https://github.com/Yikun/hub-mirror-action/blob/master/.github/workflows/verify-on-ubuntu.yml) as demo.

### 参数详解

- `src` 需要被同步的源端账户名，例如Github的kunpengcompute组织，为github/kunpengcompute。
- `dst` 需要同步到的目的端账户名，例如Gitee的kunpengcompute组织，为gitee/kunpengcompute。
- `dst_key` 用于目的端上传代码的SSH key，用于上传代码，Github可以在[这里](https://gitee.com/profile/sshkeys)找到，Gitee可以[这里](https://github.com/settings/keys)找到
- `dst_token` 创建仓库的API tokens， 用于自动创建不存在的仓库，Github可以在[这里](https://github.com/settings/tokens)找到，Gitee可以在[这里](https://gitee.com/profile/personal_access_tokens)找到。
- `account_type` 可选参数，默认为user，源和目的的账户类型，可以设置为org（组织）或者user（用户），目前仅支持同类型账户的同步。
- `clone_style` 可选参数，默认为https，可以设置为ssh或者https。

### 快速启用指南
```yaml
on: push
name: Hub Action test for org account
jobs:
  run:
    name: Run
    runs-on: ubuntu-latest
    steps:
    - name: Checkout source codes
      uses: actions/checkout@v1
    - name: Mirror Github to Gitee
      uses: ./.
      with:
        src: github/kunpengcompute
        dst: gitee/kunpengcompute
        dst_key: ${{ secrets.GITEE_PRIVATE_KEY }}
        dst_token: ${{ secrets.GITEE_TOKEN }}
        account_type: org
```
例如，我们需要在每次push时，将github的组织账号kunpengcompute同步到gitee上，就可以用上述配置。
1. **增加Token和Key**，分别获取[ssh key](https://gitee.com/profile/sshkeys)和[token](https://gitee.com/profile/personal_access_tokens)。
2. **增加Secrets配置**，在配置仓库的Setting-Secrets中新增Secrets，例如GITEE_PRIVATE_KEY、GITEE_TOKEN
3. **增加workflow文件**，在配置仓库新增workflow文件，如上。

