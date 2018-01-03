# PyPy Package Compatibility Report Generator #

To generate the report, run:

```
docker-compose build
python main.py
```

To filter the set of packages being tested, use the `--filter` option, e.g.:

```
python main.py python main.py --filter pandas scipy scikit-learn
```
