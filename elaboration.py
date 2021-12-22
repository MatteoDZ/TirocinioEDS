from snappy import ProductIO, jpy, HashMap, GPF, ProgressMonitor
import os


# B1-B9 1830
# B5-B6-B7-B8A-B11-B12 5490
# B2-B3-B4-B8 10980

# Funzione per il resampling delle bande
def resample(p):

    parameters = HashMap()
    parameters.put('targetResolution', 10)  # 10 porta a 10980, 20 porta a 5490
    print('Resampling in corso...')
    product = GPF.createProduct('Resample', parameters, p)
    print('Resampling finito')

    return product


# Funzione per la creazione di un nuovo prodotto e dell'immagine corrsipondente
def createimages(filename, path):

    p = ProductIO.readProduct(path + '/' + filename)
    product = resample(p)
    # Creazione del BandDescriptor (Cosa fa?)
    BandDescriptor = jpy.get_type('org.esa.snap.core.gpf.common.BandMathsOp$BandDescriptor')

    # Creazione delle informazioni riguardanti la banda: Nome, tipo e l'espressione per ottenerla
    targetband = BandDescriptor()
    targetband.name = 'ndvi_band'
    targetband.type = 'float32'
    targetband.expression = '(B8 - B4)/(B8 + B4)'

    # targetband1 = BandDescriptor()
    # targetband1.name = 'evi_band' # O qualunque indice si voglia usare
    # targetband1.type = 'float32'
    # targetband1.expression = '2.5 * (B8 - B4) / ((B8 + 6.0 * B4 - 7.5 * B2) + 1.0)'

    # ulteriori espressioni sono:
    # B11 / B8 -> Moisture Index (MSI)
    # (B3 - B8) / (B3 + B8) -> Normalized Difference Water Index (NDWI)
    # (B8A - B4 - y * (B4 - B2)) / (B8A + B4 - y * (B4 - B2)) NB: y = 0.106 -> Atmosferically Resistent Vegetation Index (ARVI)
    # (B8 - B4) / (B8 + B4 + L) * (1.0 + L) NB: L = 0.428 -> Soil Adjusted Vegetation Index (SAVI)

    # Creazione dell'array che ospita le bande. Si possono creare piú bande e aggiungerle tutte all'array,
    # in modo da averle tutte in un unico prodotto
    targetBands = jpy.array('org.esa.snap.core.gpf.common.BandMathsOp$BandDescriptor', 1)
    targetBands[0] = targetband

    # Creazione dell'hashmap per ospitare le bande
    parameters = HashMap()
    parameters.put('targetBands', targetBands)

    # Creazione del prodotto finale
    print('Creazione di un nuovo prodotto in corso...')
    result = GPF.createProduct('BandMaths', parameters, product)
    print('Creazione di un nuovo prodotto finita')

    # IMAGE SECTION

    # recupero delle classi File e ImageIO da java
    imageIO = jpy.get_type('javax.imageio.ImageIO')
    File = jpy.get_type('java.io.File')

    # Selezione della banda e creazione dell'immagine
    band = result.getBand('ndvi_band')
    image = band.createRgbImage(ProgressMonitor.NULL)
    name = File(path + '/images/ndvi_' + filename[11:19] + '.png')
    print('Creazione di un immagine in corso...')
    imageIO.write(image, 'PNG', name)
    print('Creazione di ndvi_' + filename[11:19] + '.png' + ' finita')

    # ProductIO.writeProduct(result, 'snappy_bmaths_output.dim', 'BEAM-DIMAP')


if __name__ == '__main__':
    path = 'D:/Download'
    for directory in os.listdir(path):
        temp_path = path + '/' + directory
        for filename in os.listdir(temp_path):
            if filename.endswith('.zip'):
                createimages(filename, temp_path)
