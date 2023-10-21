import datetime as dt
#import matplotlib.pyplot as plt

from OMIEData.DataImport.omie_marginalprice_importer import OMIEMarginalPriceFileImporter
#from OMIEData.Enums.all_enums import DataTypeInMarginalPriceFile


dateIni = dt.datetime(2020, 1, 1)
dateEnd = dt.datetime(2022, 3, 22)



df = OMIEMarginalPriceFileImporter(date_ini=dateIni, date_end=dateEnd).read_to_dataframe(verbose=True)
df.sort_values(by='DATE', axis=0, inplace=True)
print(df)