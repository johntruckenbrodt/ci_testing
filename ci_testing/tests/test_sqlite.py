from osgeo import gdal, ogr, osr
from ci_testing.sqlite_util import sqlite_setup

gdal.UseExceptions()
ogr.UseExceptions()
osr.UseExceptions()


def test_ext():
    conn = sqlite_setup(extensions=['spatialite', 'gdal'])
    assert 'execute' in dir(conn)
