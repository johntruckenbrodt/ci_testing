import os
import shutil
import pytest
import numpy as np
from osgeo import gdal, ogr, osr
from pyroSAR import identify
from pyroSAR.spatial import crsConvert, haversine, Raster, stack, ogr2ogr, gdal_translate, gdal_rasterize, Vector, bbox, intersect
from pyroSAR.spatial.vector import feature2vector, dissolve
from pyroSAR.ancillary import finder


from ci_testing.sqlite_util import sqlite_setup

gdal.UseExceptions()
ogr.UseExceptions()
osr.UseExceptions()


def test_dissolve(tmpdir):
    scene = identify('ci_testing/tests/data/S1A_IW_GRDH_1SDV_20150222T170750_20150222T170815_004739_005DD8_3768.zip')
    bbox1 = scene.bbox()
    # retrieve extent and shift its coordinates by one degree
    ext = bbox1.extent
    for key in ext.keys():
        ext[key] += 1
    # create new bbox shapefile with modified extent
    bbox2_name = os.path.join(str(tmpdir), 'bbox2.shp')
    bbox(ext, bbox1.srs, bbox2_name)
    # assert intersection between the two bboxes and combine them into one
    with Vector(bbox2_name) as bbox2:
        assert intersect(bbox1, bbox2) is not None
        bbox1.addvector(bbox2)
    # write combined bbox into new shapefile
    bbox3_name = os.path.join(str(tmpdir), 'bbox3.shp')
    bbox1.write(bbox3_name)
    bbox1.close()
    # dissolve the geometries in bbox3 and write the result to new bbox4
    bbox4_name = os.path.join(str(tmpdir), 'bbox4.shp')
    dissolve(bbox3_name, bbox4_name, field='id')
    assert os.path.isfile(bbox4_name)


def test_ext():
    conn = sqlite_setup(extensions=['spatialite', 'gdal'])
    assert 'execute' in dir(conn)
