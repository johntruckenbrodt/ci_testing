import pyroSAR
# import logging
# import unittest
import pytest
import os

testdir = os.getenv('TESTDATA_DIR', 'ci_testing/tests/data/')

testcases = [
    #SAFE
    {'path': os.path.join('ci_testing/tests/data/', 'S1A_IW_GRDH_1SDV_20150222T170750_20150222T170815_004739_005DD8_3768.zip'),
     'acquisition_mode': 'IW',
     'compression': 'zip',
     'corners': {'ymax': 52.183979, 'ymin': 50.295261, 'xmin': 8.017178, 'xmax': 12.0268},
     'lines': 16685,
     'outname': 'S1A__IW___A_20150222T170750',
     'orbit': 'A',
     'polarizations': ['VV', 'VH'],
     'product': 'GRD',
     'samples': 25368,
     'sensor': 'S1A',
     'spacing': (10.0, 9.998647),
     'start': '20150222T170750',
     'stop': '20150222T170815'
     },
    #CEOS_PSR
    {'path': os.path.join(testdir, '0000022708_001001_ALOS2015976960-140909.zip'),
     'acquisition_mode': 'FBD',
     'compression': 'zip',
     'corners': {'xmax': -62.1629744, 'xmin': -62.9005207, 'ymax': -10.6783401, 'ymin': -11.4233051},
     'lines': 13160,
     'outname': 'PSR2_FBD__A_20140909T043342',
     'orbit': 'A',
     'polarizations': ['HH', 'HV'],
     'product': '1.5',
     'samples': 12870,
     'sensor': 'PSR2',
     'spacing': (6.25, 6.25),
     'start': '20140909T043342',
     'stop': '20140909T043352'
     }
]


@pytest.fixture()
def scene(case):
    case['pyro'] = pyroSAR.identify(case['path'])
    return case


@pytest.mark.parametrize('case', testcases)
class Test_Metadata():
    def test_attributes(self, scene):
        assert scene['pyro'].acquisition_mode == scene['acquisition_mode']
        assert scene['pyro'].compression == scene['compression']
        assert scene['pyro'].getCorners() == scene['corners']
        assert scene['pyro'].lines == scene['lines']
        assert scene['pyro'].outname_base() == scene['outname']
        assert scene['pyro'].orbit == scene['orbit']
        assert scene['pyro'].polarizations == scene['polarizations']
        assert scene['pyro'].product == scene['product']
        assert scene['pyro'].samples == scene['samples']
        assert scene['pyro'].start == scene['start']
        assert scene['pyro'].stop == scene['stop']
        assert scene['pyro'].sensor == scene['sensor']
        assert scene['pyro'].spacing == scene['spacing']
        assert scene['pyro'].is_processed('data/') is False


def test_identify_fail():
    with pytest.raises(IOError):
        pyroSAR.identify(os.path.join(testdir, 'foobar'))


def test_export2dict():
    pass


'''
class TestMetadataS1(unittest.TestCase):
    def setUp(self):
        self.s1 = pyroSAR.identify('data/S1A_IW_GRDH_1SDV_20150222T170750_20150222T170815_004739_005DD8_3768.zip')
        #print self.s1.meta
    def tearDown(self):
        self.s1 = None

    def test_compression_zip(self):
        self.assertEqual(self.s1.compression, 'zip')

    def test_sensor_S1(self):
        self.assertEqual(self.s1.sensor, 'S1A')

    def test_product(self):
        self.assertEqual(self.s1.product, 'GRD')

    def test_getCorners(self):
        pass
        #self.assertEqual(self.s1.getCorners(), {'xmin':}) 

    def test_is_processed_False(self):
        self.assertFalse(self.s1.is_processed('data/'))

    def test_outname_base(self):
        self.assertEqual(self.s1.outname_base(), )

    def test_orbit(self):
        self.assertEqual(self.s1.orbit, 'A')

    #def test_

if __name__ == '__main__':
    unittest.main()
'''
