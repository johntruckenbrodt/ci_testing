
from ci_testing.sqlite_util import __Handler


def test_ext():
    handler = __Handler(extensions=['spatialite', 'gdal'])
    assert len(handler.extensions) == 2
