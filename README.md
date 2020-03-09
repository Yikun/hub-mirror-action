# Hub Mirror Action
The action to mirror the organization repos between hub(github/gitee).

# Usage

See [action.yml](action.yml)

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

As above, the action will do mirror update from github/kunpengcompute to gitee/kunpengcompute.

You could take a look on the [verify workflow](https://github.com/Yikun/hub-mirror-action/blob/master/.github/workflows/verify-on-ubuntu.yml) as demo.

# Note

- For gittee as destination：

  - dst_key: https://gitee.com/profile/sshkeys

  - dst_token: https://gitee.com/profile/personal_access_tokens

- For github as destination：

  - dst_key: https://github.com/settings/keys

  - dst_token: https://github.com/settings/tokens
