

class Hub(object):
    def __init__(
        self, src, dst
    ):
        # 切分/前后的 域名 和 用户
        self.src_type, self.src_account = src.split('/')
        self.dst_type, self.dst_account = dst.split('/')
        prefix = 'git@'
        suffix = ':'
        self.src_repo_base = prefix + self.src_type + suffix + self.src_account
        self.dst_repo_base = prefix + self.dst_type + suffix + self.dst_account
