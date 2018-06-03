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


def test_crsConvert():
    assert crsConvert(crsConvert(4326, 'wkt'), 'proj4') == '+proj=longlat +datum=WGS84 +no_defs '
    assert crsConvert(crsConvert(4326, 'prettyWkt'), 'opengis') == 'http://www.opengis.net/def/crs/EPSG/0/4326'
    assert crsConvert('+proj=longlat +datum=WGS84 +no_defs ', 'epsg') == 4326
    assert crsConvert('http://www.opengis.net/def/crs/EPSG/0/4326', 'epsg') == 4326
    assert crsConvert(crsConvert('http://www.opengis.net/def/crs/EPSG/0/4326', 'osr'), 'epsg') == 4326
    with pytest.raises(TypeError):
        crsConvert('xyz', 'epsg')
    with pytest.raises(ValueError):
        crsConvert(4326, 'xyz')


def test_haversine():
    assert haversine(50, 10, 51, 10) == 111194.92664455889


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
