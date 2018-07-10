import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def indexDataFrame(df, indexColumns, retainCols=False):
    if retainCols == True:
        df.set_index(indexColumns, drop=False, inplace=True)
    else:
        df.set_index(indexColumns, drop=True, inplace=True)

if __name__ == '__main__':

    filepath = 'C:\\Users\\lb14g16\Project 1\datafiles\cddb.h5'

    indexes = pd.read_hdf(filepath, 'indexes')
    journeyDf = pd.read_hdf(filepath, 'journeyDf')
    # Note that one of the leg indexes (TiplocIndex) is used in model calibration
    # and must therefore be retained as a separate column.  Hence for the journey
    # dataframe, the columns are not dropped
    indexDataFrame(journeyDf, indexes.tolist(), retainCols=True)
    vehicleDf = pd.read_hdf(filepath, 'vehicleDf')
    indexDataFrame(vehicleDf, indexes.tolist(), retainCols=False)
    try:
        trainDf = pd.read_hdf(filepath, 'trainDf')
        indexDataFrame(trainDf, indexes.tolist(), retainCols=False)
    except:
        pass

    print('finished')

trainjournDf = pd.concat([journeyDf,trainDf], axis=1, sort='false')
no_loadweigh = trainjournDf.loadweigh.isnull().sum()
print no_loadweigh, 'trains have given no loadweigh data'

print trainjournDf.loc[:,['UniqueJourneyId','tiplocIndex']][trainjournDf.loadweigh.isnull()==True]
