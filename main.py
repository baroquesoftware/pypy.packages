from multiprocessing import Pool

import subprocess
import os
import json
import shutil
import xmlrpclib

PYPI = xmlrpclib.ServerProxy('https://pypi.python.org/pypi')
PATH = "/tmp/pypy.space"
PIP_CACHE = "/tmp/pipcache"
DOWNLOAD_PROCESSES = 10


def thing(args):
    name, count = args
    p = subprocess.Popen('docker run -v %s:/pipcache pypyspace pypy -m pip --cache-dir=/pipcache install %s' % (PIP_CACHE, name),
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    stdout, _ = p.communicate()

    print "=" * 30, name, p.returncode, "=" * 30
    print stdout

    return name, p.returncode, stdout, count


if __name__ == '__main__':

    if os.path.exists(PATH):
        shutil.rmtree(PATH)

    os.makedirs(PATH)

    pool = Pool(processes=DOWNLOAD_PROCESSES)
    results = pool.map(thing, PYPI.top_packages(1000))
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
