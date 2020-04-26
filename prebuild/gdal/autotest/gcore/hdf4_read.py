#!/usr/bin/env pytest
###############################################################################
# $Id$
#
# Project:  GDAL/OGR Test Suite
# Purpose:  Test basic read support for a all datatypes from a HDF file.
# Author:   Andrey Kiselev, dron@remotesensing.org
#
###############################################################################
# Copyright (c) 2003, Andrey Kiselev <dron@remotesensing.org>
# Copyright (c) 2009-2012, Even Rouault <even dot rouault at spatialys.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
###############################################################################


import pytest

import gdaltest
from osgeo import gdal

pytestmark = pytest.mark.require_driver('HDF4')

init_list = [
    ('byte_3.hdf', 4672),
    ('int16_3.hdf', 4672),
    ('uint16_3.hdf', 4672),
    ('int32_3.hdf', 4672),
    ('uint32_3.hdf', 4672),
    ('float32_3.hdf', 4672),
    ('float64_3.hdf', 4672),
    ('utmsmall_3.hdf', 50054),
    ('byte_2.hdf', 4672),
    ('int16_2.hdf', 4672),
    ('uint16_2.hdf', 4672),
    ('int32_2.hdf', 4672),
    ('uint32_2.hdf', 4672),
    ('float32_2.hdf', 4672),
    ('float64_2.hdf', 4672),
    ('utmsmall_2.hdf', 50054)]


@pytest.mark.parametrize(
    'filename,checksum',
    init_list,
    ids=[tup[0].split('.')[0] for tup in init_list],
)
@pytest.mark.require_driver('HDF4Image')
def test_hdf4_open(filename, checksum):
    ut = gdaltest.GDALTest('HDF4Image', filename, 1, checksum)
    ut.testOpen()


###############################################################################
# Test reading a GR dataset


def test_hdf4_read_gr():

    # Generated by https://support.hdfgroup.org/ftp/HDF/HDF_Current/src/unpacked/hdf/examples/GR_create_and_write_image.c
    ds = gdal.Open('data/General_RImages.hdf')
    assert ds
    assert ds.RasterCount == 2
    assert ds.GetRasterBand(1).Checksum() == 361
    assert not ds.GetRasterBand(1).GetColorTable()
    assert ds.GetRasterBand(2).Checksum() == 400

###############################################################################
# Test reading a GR dataset with a palette


def test_hdf4_read_gr_palette():

    # Generated by https://support.hdfgroup.org/ftp/HDF/HDF_Current/src/unpacked/hdf/examples/GR_write_palette.c
    ds = gdal.Open('data/Image_with_Palette.hdf')
    assert ds
    assert ds.RasterCount == 1
    assert ds.GetRasterBand(1).GetColorTable()

###############################################################################
# Test HDF4_SDS with single subdataset


def test_hdf4_read_online_1():

    gdaltest.hdf4_drv = gdal.GetDriverByName('HDF4')

    if gdaltest.hdf4_drv is None:
        pytest.skip()

    if not gdaltest.download_file('http://download.osgeo.org/gdal/data/hdf4/A2004259075000.L2_LAC_SST.hdf', 'A2004259075000.L2_LAC_SST.hdf'):
        pytest.skip()

    tst = gdaltest.GDALTest('HDF4Image', 'tmp/cache/A2004259075000.L2_LAC_SST.hdf', 1, 28189, filename_absolute=1)

    return tst.testOpen()

###############################################################################
# Test HDF4_SDS with GEOLOCATION info


def test_hdf4_read_online_2():

    if gdaltest.hdf4_drv is None:
        pytest.skip()

    if not gdaltest.download_file('http://download.osgeo.org/gdal/data/hdf4/A2006005182000.L2_LAC_SST.x.hdf', 'A2006005182000.L2_LAC_SST.x.hdf'):
        pytest.skip()

    tst = gdaltest.GDALTest('HDF4Image', 'HDF4_SDS:UNKNOWN:"tmp/cache/A2006005182000.L2_LAC_SST.x.hdf":13', 1, 13209, filename_absolute=1)

    tst.testOpen()

    ds = gdal.Open('HDF4_SDS:UNKNOWN:"tmp/cache/A2006005182000.L2_LAC_SST.x.hdf":13')
    md = ds.GetMetadata('GEOLOCATION')
    ds = None

    assert md['X_DATASET'] == 'HDF4_SDS:UNKNOWN:"tmp/cache/A2006005182000.L2_LAC_SST.x.hdf":11', \
        'Did not get expected X_DATASET'


###############################################################################
# Test HDF4_EOS:EOS_GRID

def test_hdf4_read_online_3():

    if gdaltest.hdf4_drv is None:
        pytest.skip()

    if not gdaltest.download_file('http://download.osgeo.org/gdal/data/hdf4/MO36MW14.chlor_MODIS.ADD2001089.004.2002186190207.hdf', 'MO36MW14.chlor_MODIS.ADD2001089.004.2002186190207.hdf'):
        pytest.skip()

    tst = gdaltest.GDALTest('HDF4Image', 'tmp/cache/MO36MW14.chlor_MODIS.ADD2001089.004.2002186190207.hdf', 1, 34723, filename_absolute=1)

    tst.testOpen()

    ds = gdal.Open('tmp/cache/MO36MW14.chlor_MODIS.ADD2001089.004.2002186190207.hdf')
    gt = ds.GetGeoTransform()
    expected_gt = [-180.0, 0.3515625, 0.0, 90.0, 0.0, -0.3515625]
    for i in range(6):
        assert gt[i] == pytest.approx(expected_gt[i], abs=1e-8), 'did not get expected gt'

    srs = ds.GetProjectionRef()
    assert srs.find('Clarke') != -1, 'did not get expected projection'

    ds = None

###############################################################################
# Test HDF4_SDS:SEAWIFS_L1A


def test_hdf4_read_online_4():

    if gdaltest.hdf4_drv is None:
        pytest.skip()

    if not gdaltest.download_file('http://download.osgeo.org/gdal/data/hdf4/S2002196124536.L1A_HDUN.BartonBendish.extract.hdf', 'S2002196124536.L1A_HDUN.BartonBendish.extract.hdf'):
        pytest.skip()

    tst = gdaltest.GDALTest('HDF4Image', 'tmp/cache/S2002196124536.L1A_HDUN.BartonBendish.extract.hdf', 1, 33112, filename_absolute=1)

    tst.testOpen()

    ds = gdal.Open('tmp/cache/S2002196124536.L1A_HDUN.BartonBendish.extract.hdf')
    assert ds.RasterCount == 8, 'did not get expected band number'

    ds = None

###############################################################################
# Test fix for #2208


def test_hdf4_read_online_5():

    if gdaltest.hdf4_drv is None:
        pytest.skip()

    # 13 MB
    if not gdaltest.download_file('ftp://data.nodc.noaa.gov/pub/data.nodc/pathfinder/Version5.0/Monthly/1991/199101.s04m1pfv50-sst-16b.hdf', '199101.s04m1pfv50-sst-16b.hdf'):
        pytest.skip()

    tst = gdaltest.GDALTest('HDF4Image', 'tmp/cache/199101.s04m1pfv50-sst-16b.hdf', 1, 41173, filename_absolute=1)

    tst.testOpen()

###############################################################################
# Test fix for #3386 where block size is dataset size


def test_hdf4_read_online_6():

    if gdaltest.hdf4_drv is None:
        pytest.skip()

    # 1 MB
    if not gdaltest.download_file('http://download.osgeo.org/gdal/data/hdf4/MOD09Q1G_EVI.A2006233.h07v03.005.2008338190308.hdf', 'MOD09Q1G_EVI.A2006233.h07v03.005.2008338190308.hdf'):
        pytest.skip()

    # Test with quoting of components
    tst = gdaltest.GDALTest('HDF4Image', 'HDF4_EOS:EOS_GRID:"tmp/cache/MOD09Q1G_EVI.A2006233.h07v03.005.2008338190308.hdf":"MODIS_NACP_EVI":"MODIS_EVI"', 1, 12197, filename_absolute=1)

    tst.testOpen()

    ds = gdal.Open('HDF4_EOS:EOS_GRID:tmp/cache/MOD09Q1G_EVI.A2006233.h07v03.005.2008338190308.hdf:MODIS_NACP_EVI:MODIS_EVI')

    if 'GetBlockSize' in dir(gdal.Band):
        (blockx, blocky) = ds.GetRasterBand(1).GetBlockSize()
        assert blockx == 4800 and blocky == 4800, "Did not get expected block size"

    cs = ds.GetRasterBand(1).Checksum()
    assert cs == 12197, 'did not get expected checksum'

    ds = None

###############################################################################
# Test fix for #3386 where block size is smaller than dataset size


def test_hdf4_read_online_7():

    if gdaltest.hdf4_drv is None:
        pytest.skip()

    # 4 MB
    if not gdaltest.download_file('http://download.osgeo.org/gdal/data/hdf4/MOD09A1.A2010041.h06v03.005.2010051001103.hdf', 'MOD09A1.A2010041.h06v03.005.2010051001103.hdf'):
        pytest.skip()

    tst = gdaltest.GDALTest('HDF4Image', 'HDF4_EOS:EOS_GRID:tmp/cache/MOD09A1.A2010041.h06v03.005.2010051001103.hdf:MOD_Grid_500m_Surface_Reflectance:sur_refl_b01', 1, 54894, filename_absolute=1)

    tst.testOpen()

    ds = gdal.Open('HDF4_EOS:EOS_GRID:tmp/cache/MOD09A1.A2010041.h06v03.005.2010051001103.hdf:MOD_Grid_500m_Surface_Reflectance:sur_refl_b01')

    if 'GetBlockSize' in dir(gdal.Band):
        (blockx, blocky) = ds.GetRasterBand(1).GetBlockSize()
        assert blockx == 2400 and blocky == 32, "Did not get expected block size"

    cs = ds.GetRasterBand(1).Checksum()
    assert cs == 54894, 'did not get expected checksum'

    ds = None


###############################################################################
# Test reading a HDF4_EOS:EOS_GRID where preferred block height reported would be 1
# but that will lead to very poor performance (#3386)

def test_hdf4_read_online_8():

    if gdaltest.hdf4_drv is None:
        pytest.skip()

    # 5 MB
    if not gdaltest.download_file('https://e4ftl01.cr.usgs.gov/MOLT/MOD13Q1.006/2006.06.10/MOD13Q1.A2006161.h34v09.006.2015161173716.hdf', 'MOD13Q1.A2006161.h34v09.006.2015161173716.hdf'):
        pytest.skip()

    tst = gdaltest.GDALTest('HDF4Image', 'HDF4_EOS:EOS_GRID:tmp/cache/MOD13Q1.A2006161.h34v09.006.2015161173716.hdf:MODIS_Grid_16DAY_250m_500m_VI:250m 16 days NDVI', 1, 44174, filename_absolute=1)

    tst.testOpen()

    ds = gdal.Open('HDF4_EOS:EOS_GRID:tmp/cache/MOD13Q1.A2006161.h34v09.006.2015161173716.hdf:MODIS_Grid_16DAY_250m_500m_VI:250m 16 days NDVI')

    cs = ds.GetRasterBand(1).Checksum()
    assert cs == 44174, 'did not get expected checksum'

    if 'GetBlockSize' in dir(gdal.Band):
        (blockx, blocky) = ds.GetRasterBand(1).GetBlockSize()
        if blockx != 4800 or blocky == 1:
            print('blockx=%d, blocky=%d' % (blockx, blocky))
            pytest.fail("Did not get expected block size")

    ds = None

###############################################################################
# Test reading L1G MTL metadata metadata


def test_hdf4_read_online_9():

    if gdaltest.hdf4_drv is None:
        pytest.skip()

    if not gdaltest.download_file('http://www.geogratis.cgdi.gc.ca/download/landsat_7/hdf/L71002025_02520010722/L71002025_02520010722_MTL.L1G', 'L71002025_02520010722_MTL.L1G'):
        pytest.skip()

    if not gdaltest.download_file('http://www.geogratis.cgdi.gc.ca/download/landsat_7/hdf/L71002025_02520010722/L71002025_02520010722_HDF.L1G', 'L71002025_02520010722_HDF.L1G'):
        pytest.skip()

    f = open('tmp/cache/L71002025_02520010722_B10.L1G', 'wb')
    f.close()

    ds = gdal.Open('HDF4_SDS:UNKNOWN:"tmp/cache/L71002025_02520010722_HDF.L1G":0')
    gcp_count = ds.GetGCPCount()
    ds = None

    assert gcp_count == 4, 'did not get expected gcp count'

###############################################################################
# Test that non-tiled access works (#4672)


def test_hdf4_read_online_10():

    if gdaltest.hdf4_drv is None:
        pytest.skip()

    if not gdaltest.download_file('http://trac.osgeo.org/gdal/raw-attachment/ticket/4672/MOD16A2.A2000M01.h14v02.105.2010357183410.hdf', 'MOD16A2.A2000M01.h14v02.105.2010357183410.hdf'):
        pytest.skip()

    ds = gdal.Open('HDF4_EOS:EOS_GRID:"tmp/cache/MOD16A2.A2000M01.h14v02.105.2010357183410.hdf":MOD_Grid_MOD16A2:ET_1km')

    if 'GetBlockSize' in dir(gdal.Band):
        (blockx, blocky) = ds.GetRasterBand(1).GetBlockSize()
        assert blockx == 1200 and blocky == 833, "Did not get expected block size"

    cs = ds.GetRasterBand(1).Checksum()
    assert cs == 20976, 'did not get expected checksum'

    ds = None



###############################################################################
# Test reading HDFEOS SWATH projducts


def test_hdf4_read_online_11():

    if gdaltest.hdf4_drv is None:
        pytest.skip()

    if not gdaltest.download_file('https://gamma.hdfgroup.org/ftp/pub/outgoing/NASAHDFfiles2/eosweb/hdf4/hdfeos2-swath-wo-dimmaps/AMSR_E_L2_Ocean_B01_200206182340_A.hdf', 'AMSR_E_L2_Ocean_B01_200206182340_A.hdf'):
        pytest.skip()

    ds = gdal.Open('HDF4_EOS:EOS_SWATH:"tmp/cache/AMSR_E_L2_Ocean_B01_200206182340_A.hdf":Swath1:Ocean_products_quality_flag')

    cs = ds.GetRasterBand(1).Checksum()
    assert cs == 7809, 'did not get expected checksum'