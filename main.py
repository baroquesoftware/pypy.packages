from __future__ import print_function

import argparse
import json
import os
import shutil
import subprocess
import xmlrpclib
from multiprocessing.dummy import Pool

PYPI = xmlrpclib.ServerProxy('https://pypi.python.org/pypi')
PATH = "/tmp/pypy.space"
PIP_CACHE = "/tmp/pipcache"
REQUIREMENTS_DIR = 'requirements'
REQUIREMENTS_HOST_DIR = os.path.join(os.getcwd(), REQUIREMENTS_DIR)
REQUIREMENTS_CONTAINER_DIR = os.path.join('/root', REQUIREMENTS_DIR)

BASE_DOCKER_COMMAND = [
    'docker', 'run',
    '-v', '{}:{}'.format(
        REQUIREMENTS_HOST_DIR, REQUIREMENTS_CONTAINER_DIR),
    '-v', '{}:/pipcache'.format(PIP_CACHE),
    'pypypackages_pypy:latest'
]
BASE_PIP_CMD = ['pip', '--cache-dir=/pipcache', 'install']

def thing(args):
    name, count = args
    requirements_file = os.path.join('requirements', name)
    if os.path.isfile(requirements_file):
        pip_cmd = BASE_PIP_CMD + ['-r', requirements_file]
    else:
        pip_cmd = BASE_PIP_CMD + [name]
    p = subprocess.Popen(BASE_DOCKER_COMMAND + pip_cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    stdout, _ = p.communicate()

    print("=" * 30, name, p.returncode, "=" * 30)
    print(stdout)

    return name, p.returncode, stdout, count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--parallel', help='Number of concurrent processes', type=int,
        default=50)
    parser.add_argument(
        '--filter', nargs='*',
        help='Filter to these packages')
    args = parser.parse_args()

    if os.path.exists(PATH):
        shutil.rmtree(PATH)

    os.makedirs(PATH)

    pool = Pool(processes=args.parallel)
    top_packages = PYPI.top_packages(1000)
    if args.filter:
        filter_ = {p for p in args.filter}
        top_packages = [p for p in top_packages if p[0] in filter_]
    results = pool.map(thing, top_packages)
    pool.close()
    pool.join()

    index = []

    for name, status, output, count in results:
        output_log = '%s.txt' % name

        with open(os.path.join(PATH, output_log), 'w') as f:
            f.write(output)

        index.append((name, {"status": status,
                             "count": count,
                             "log": output_log}))

    json.dump(index, open(os.path.join(PATH, "index.json"), 'w'), indent=2)

if __name__ == '__main__':
    main()
