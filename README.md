# PyPy Package Compatibility Report Generator #

The source for http://packages.pypy.org/, it downloads and installs the top 1000 PYPI packages into pypy,
and records success or failure

To generate the report, run:

```
docker-compose build
python main.py
```

To filter the set of packages being tested, use the `--filter` option, e.g.:

```
python main.py python main.py --filter pandas scipy scikit-learn
```
