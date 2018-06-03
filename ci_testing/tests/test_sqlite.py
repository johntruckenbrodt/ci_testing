
from ci_testing.sqlite_util import sqlite_setup


def test_ext():
    conn = sqlite_setup(extensions=['spatialite', 'gdal'])
    assert 'execute' in dir(conn)
