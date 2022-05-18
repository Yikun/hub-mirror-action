# Pub Hub Mirror Action

简体中文 | [English](./README_en.md)

一个用于在hub间（例如Github，Gitee、Coding，不局限，可以是所有）账户代码仓库同步的action，这个项目脱胎于Yikun/hub-mirror-action@master。

简单做几点说明：
1、由于我是想要一个纯粹的不同的hub之间 同步的脚本，所以将该脚本进行了删减，不是作者做的不好，只是我仅仅需要简单的功能罢了
2、目前只支持，也只会支持两个仓库必须在两个hub之间存在的情况，不再创建新的仓库（由于创建仓库需要api支持，但是为了更通用，所以决定不支持对应的功能）
3、根据能量守恒定律，失去些什么，必然能得到些什么，这样就可以在不同的hub之间同步数据，不管是 从 github->gitee 还是 gitee-github 都可以支持到
4、src、dst 都需要写全路径了，例如：github.com/kunpengcompute
5、static_list 是必传参数，因为不会再动态获取对应的repos了
6、dst_key 也是必传参数，因为为了安全考虑，我决定全部使用ssh的方式进行同步，如果后期有需要，可以兼容https

## 用法

```yaml
steps:
- name: Mirror the Github organization repos to Gitee.
  uses: Dislazy/hub-mirror-action@master
  with:
    src: github.com/kunpengcompute
    dst: gitee.com/kunpengcompute
    dst_key: ${{ secrets.GITEE_PRIVATE_KEY }}
    static_list: repo1,repo2,repo3
    cache_path: /github/workspace/hub-mirror-cache
    force_update: true
    debug: true
    timeout: '1h'
    mappings: "yikun.github.com=>blog"
```

上面的配置完成了kunpencompute组织从github到gitee的同步，你可以在[测试和demo](https://github.com/dislazy/hub-mirror-action/tree/master/.github/workflows)找到完整用法。


## 参数详解
#### 必选参数
- `src` 需要被同步的源端账户名，如github.com/kunpengcompute，表示Github的kunpengcompute账户。
- `dst` 需要同步到的目的端账户名，如gitee.com/kunpengcompute，表示Gitee的kunpengcompute账户。
- `dst_key` 用于在目的端上传代码的私钥(默认可以从~/.ssh/id_rsa获取），可参考[生成/添加SSH公钥](https://gitee.com/help/articles/4181)或[generating SSH keys](https://docs.github.com/articles/generating-an-ssh-key/)生成，并确认对应公钥已经被正确配置在目的端。对应公钥，Github可以在[这里](https://github.com/settings/keys)配置，Gitee可以[这里](https://gitee.com/profile/sshkeys)配置。
- `static_list` 默认为'', 配置后，仅同步静态列表，不会再动态获取需同步列表，如“repo1,repo2,repo3”。

#### 可选参数
- `cache_path` 默认为'', 将代码缓存在指定目录，用于与actions/cache配合以加速镜像过程。
- `force_update` 默认为false, 配置后，启用git push -f强制同步，**注意：开启后，会强制覆盖目的端仓库**。
- `debug` 默认为false, 配置后，启用debug开关，会显示所有执行命令。
- `timeout` 默认为'30m', 用于设置每个git命令的超时时间，'600'=>600s, '30m'=>30 mins, '1h'=>1 hours
- `mappings` 源仓库映射规则，比如'A=>B, C=>CC', A会被映射为B，C会映射为CC，映射不具有传递性。主要用于源和目的仓库名不同的镜像。

## FAQ

- 如何在secrets添加dst_key？
  下面是添加secrets的方法，也可以参考[secrets官方文档](https://help.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets)了解更多：
  2. **增加Secrets配置**，在配置仓库的Setting-Secrets中新增Secrets，例如GITEE_PRIVATE_KEY、GITEE_TOKEN
  3. **在Workflow中引用**， 可以用过类似`${{ secrets.GITEE_PRIVATE_KEY }}`来访问

## 参考
- [Hub mirror template](https://github.com/yi-Xu-0100/hub-mirror): 一个用于展示如何使用这个action的模板仓库. from @yi-Xu-0100
- [自动镜像 GitHub 仓库到 Gitee](https://github.com/ShixiangWang/sync2gitee): 一个关于如何使用这个action的介绍. from @ShixiangWang
- [巧用Github Action同步代码到Gitee](http://yikun.github.io/2020/01/17/%E5%B7%A7%E7%94%A8Github-Action%E5%90%8C%E6%AD%A5%E4%BB%A3%E7%A0%81%E5%88%B0Gitee/): Github Action第一篇软文
- [Hub Mirror Action](https://github.com/Yikun/hub-mirror-action): 该仓库的前身仓库，棒极了
## 最后

如果觉得不错，**来个star**支持下作者吧！你的Star是我更新代码的动力！：）

想任何想吐槽或者建议的都可以直接飞个[issue](https://github.com/dislazy/hub-mirror-action/issues).

