import argparse
import sys
import yaml

from utils import str2bool, str2list, str2map
from hub import Hub
from mirror import Mirror


class HubMirror(object):
    def __init__(self):
        self.parser = self._create_parser()
        self.args = self.parser.parse_args()
        self.static_list = str2list(self.args.static_list)
        self.mappings = str2map(self.args.mappings)

    def _create_parser(self):
        with open('/action.yml', 'r') as f:
            action = yaml.safe_load(f)
        parser = argparse.ArgumentParser(
            description=action['description'])
        inputs = action['inputs']

        for key in inputs:
            if key in ['dst_key']:
                continue
            input_args = inputs[key]
            dft = input_args.get('default', '')
            parser.add_argument(
                "--" + key.replace('_', '-'),
                # Autofill the `type` according `default`, str by default
                type=str2bool if isinstance(dft, bool) else str,
                required=input_args.get('required', False),
                default=dft,
                help=input_args.get('description', '')
            )
        return parser

    def run(self):
        hub = Hub(
            self.args.src,
            self.args.dst
        )

        # Using static list when static_list is set
        repos = self.static_list
        src_repos = repos if repos else []

        total, success, skip = len(src_repos), 0, 0
        failed_list = []
        for src_repo in src_repos:
            # Set dst_repo to src_repo mapping or src_repo directly
            dst_repo = self.mappings.get(src_repo, src_repo)
            print("Map %s to %s" % (src_repo, dst_repo))
            print("Backup %s" % src_repo)
            try:
                mirror = Mirror(
                    hub, src_repo, dst_repo,
                    cache=self.args.cache_path,
                    timeout=self.args.timeout,
                    force_update=self.args.force_update,
                    )
                mirror.download()
                mirror.create()
                mirror.push()
                success += 1
            except Exception as e:
                print(e)
                failed_list.append(src_repo)

        failed = total - success - skip
        res = (total, skip, success, failed)
        print("Total: %s, skip: %s, successed: %s, failed: %s." % res)
        print("Failed: %s" % failed_list)
        if failed_list:
            sys.exit(1)


if __name__ == '__main__':
    mirror = HubMirror()
    mirror.run()
