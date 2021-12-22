from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import datetime, timedelta
import os

# Chiavi per l'accesso alla piattaforma scihub di copernicus
api = SentinelAPI('matteodz', '3jqUDsu43DNYmQ_', 'https://scihub.copernicus.eu/dhus')
api5p = SentinelAPI(user='s5pguest', password='s5pguest', api_url='https://s5phub.copernicus.eu/dhus')


# Funzione per il download dei prodotti di sentinel-2
def downloadS2():
    footprintC = geojson_to_wkt(read_geojson('D:/Download/GeoJson/mapC.geojson'))
    footprintW = geojson_to_wkt(read_geojson('D:/Download/GeoJson/mapO.geojson'))
    footprintN = geojson_to_wkt(read_geojson('D:/Download/GeoJson/mapN.geojson'))
    # footprintE = geojson_to_wkt(read_geojson('D:/Download/GeoJson/mapE.geojson'))
    footprintS = geojson_to_wkt(read_geojson('D:/Download/GeoJson/mapS.geojson'))

    yd = datetime.today() - timedelta(days=1)

    productC = api.query(footprintC,
                         date=(yd.strftime('%Y%m%d'), 'NOW/DAY'),
                         # date=("20210601", "20210901"),
                         platformname='Sentinel-2',
                         cloudcoverpercentage=(0, 100),
                         producttype='S2MSI2A')

    productW = api.query(footprintW,
                         date=(yd.strftime('%Y%m%d'), 'NOW/DAY'),
                         # date=("20210601", "20210901"),
                         platformname='Sentinel-2',
                         cloudcoverpercentage=(0, 100),
                         producttype='S2MSI2A')

    productN = api.query(footprintN,
                         date=(yd.strftime('%Y%m%d'), 'NOW/DAY'),
                         # date=("20210601", "20210901"),
                         platformname='Sentinel-2',
                         cloudcoverpercentage=(0, 100),
                         producttype='S2MSI2A')

    # productE = api.query(footprintE,
    #                     date=(yd.strftime('%Y%m%d'), 'NOW/DAY'),
    #                     # date=("20210601", "20210901"),
    #                     platformname='Sentinel-2',
    #                     cloudcoverpercentage=(0, 100),
    #                     producttype='S2MSI2A')

    productS = api.query(footprintS,
                         date=(yd.strftime('%Y%m%d'), 'NOW/DAY'),
                         # date=("20210601", "20210901"),
                         platformname='Sentinel-2',
                         cloudcoverpercentage=(0, 100),
                         producttype='S2MSI2A')

    print("Downloading SettoreCentro")
    api.download_all(productC, directory_path='D:/Download/SettoreCentro')
    print("Downloading SettoreOvest")
    api.download_all(productW, directory_path='D:/Download/SettoreOvest')
    print("Downloading SettoreNord")
    api.download_all(productN, directory_path='D:/Download/SettoreNord')
    # print("Downloading SettoreEst")
    # api.download_all(productE, directory_path='D:/Download/SettoreEst')
    print("Downloading SettoreSud")
    api.download_all(productS, directory_path='D:/Download/SettoreSud')


# Funzione per il download dei prodotti di sentinel-3
def downloadS3():
    footprint = geojson_to_wkt(read_geojson('D:/Download/GeoJson/mapC.geojson'))
    yd = datetime.today() - timedelta(days=1)

    product3_OLCI_LFR = api.query(footprint,
                                  date=(yd.strftime('%Y%m%d'), 'NOW/DAY'),
                                  # date=("20210601", "20210901"),
                                  platformname='Sentinel-3',
                                  cloudcoverpercentage=(0, 100),
                                  producttype='OL_2_LFR___')

    product3_SLSTR = api.query(footprint,
                               date=(yd.strftime('%Y%m%d'), 'NOW/DAY'),
                               # date=("20210601", "20210901"),
                               platformname='Sentinel-3',
                               cloudcoverpercentage=(0, 100),
                               producttype='SL_2_LST___')

    print("Downloading sentinel-3 OLCI_product")
    api.download_all(product3_OLCI_LFR, directory_path='D:/Download/Sentinel3_OLCI')
    print("Downloading sentinel-3 SLSTR_product")
    api.download_all(product3_SLSTR, directory_path='D:/Download/Sentinel3_SLSTR')


# Funzione per il download dei prodotti di sentinel-5p
def downloadS5P():
    footprint = geojson_to_wkt(read_geojson('D:/Download/GeoJson/mapC.geojson'))
    yd = datetime.today() - timedelta(days=1)

    product_5p = api5p.query(area=footprint,
                             date=(yd.strftime('%Y%m%d'), 'NOW/DAY'),
                             # date=("20210601", "20210901"),
                             platformname='Sentinel-5',
                             producttype='L2__NO2___'
                             )

    api5p.download_all(product_5p, directory_path='D:/Download/Sentinel5p')


if __name__ == '__main__':
    downloadS2()
    # downloadS3()
    # ownloadS5P()
