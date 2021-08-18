import argparse
import git


class Progress(git.remote.RemoteProgress):
    def __init__(self, name):
        super(Progress, self).__init__()
        self.name = name

    def update(self, op_code, cur_count, max_count=None, message=''):
        print('Process %s, %s' % (self.name, self._cur_line))


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def cov2sec(s):
    _h = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
    if _h.get(s[-1]):
        return int(s[:-1]) * _h.get(s[-1], 1)
    else:
        return int(s)


def str2list(s):
    # Change "a, b" to ['a', 'b']
    if not s:
        return []
    return s.replace(' ', '').split(',') if s else []


# "a=>b, c=>d" to {'a': 'b', 'c': 'd'}
def str2map(s):
    if not s:
        return {}
    mappings = {}
    mappings_list = str2list(s)
    for maping in mappings_list:
        old, new = maping.split("=>")
        mappings[old] = new
    return mappings
