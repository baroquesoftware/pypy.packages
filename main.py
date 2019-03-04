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

virtualenv_name = None

BASE_DOCKER_COMMAND = [
    'docker', 'run',
    '-v', '{}:{}'.format(
        REQUIREMENTS_HOST_DIR, REQUIREMENTS_CONTAINER_DIR),
    '-v', '{}:/pipcache'.format(PIP_CACHE),
    'pypypackages_pypy:latest'
]

def thing(args):
    name, count = args
    print("=" * 30, name, 'starting pip install', '='*30)
    base_pip_cmd = [
        os.path.join(virtualenv_name, 'bin/pip'),
        '--cache-dir=/pipcache',
        'install']
    requirements_file = os.path.join('requirements', name)
    if os.path.isfile(requirements_file):
        pip_cmd = base_pip_cmd + ['-r', requirements_file]
    else:
        pip_cmd = base_pip_cmd + [name]
    p = subprocess.Popen(BASE_DOCKER_COMMAND + pip_cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    stdout, _ = p.communicate()

    print("=" * 30, name, p.returncode, "=" * 30)
    print(stdout)

    return name, p.returncode, stdout, count


def main():
    global virtualenv_name
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--parallel', help='Number of concurrent processes', type=int,
        default=50)
    parser.add_argument(
        '--filter', nargs='*',
        help='Filter to these packages')
    parser.add_argument(
        '--virtualenv', default='pypy3_venv',
        help='Python virtualenv for package installation')
    args = parser.parse_args()
    virtualenv_name = args.virtualenv

    if os.path.exists(PATH):
        shutil.rmtree(PATH)

    os.makedirs(PATH)

    pool = Pool(processes=args.parallel)
    top_packages = []

    with open('downloads.csv', 'rt') as fid:
        for line in fid:
            try:
                vals = line.split(',')
                top_packages.append((vals[0], int(vals[1])))
            except:
                continue
    if args.filter:
        filter_ = {p for p in args.filter}
        top_packages = [p for p in top_packages if p[0] in filter_]
    results = pool.map(thing, top_packages)
    pool.close()
    pool.join()

    p = subprocess.Popen(BASE_DOCKER_COMMAND + [
                        os.path.join(virtualenv_name, 'bin/python'), '-c',
                        "import sys, %s; print(sys.version)" % (top_packages[-1][0],),],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    stdout, stderr = p.communicate()

    print("=" * 30, 'python', "=" * 30)
    print(stdout)
    print(stderr)
    print("=" * 30, 'python', "=" * 30)

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
