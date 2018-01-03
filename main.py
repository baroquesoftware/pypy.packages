from multiprocessing import Pool

import argparse
import subprocess
import os
import json
import shutil
import xmlrpclib

PYPI = xmlrpclib.ServerProxy('https://pypi.python.org/pypi')
PATH = "/tmp/pypy.space"
PIP_CACHE = "/tmp/pipcache"
DOWNLOAD_PROCESSES = 50


def thing(args):
    name, count = args
    p = subprocess.Popen('docker run -v %s:/pipcache pypypackages_pypy:latest pypy_venv/bin/pip --cache-dir=/pipcache install %s' % (PIP_CACHE, name),
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    stdout, _ = p.communicate()

    print "=" * 30, name, p.returncode, "=" * 30
    print stdout

    return name, p.returncode, stdout, count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--filter', nargs='*', help='Filter to these packages')
    args = parser.parse_args()

    if os.path.exists(PATH):
        shutil.rmtree(PATH)

    os.makedirs(PATH)

    pool = Pool(processes=DOWNLOAD_PROCESSES)
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
