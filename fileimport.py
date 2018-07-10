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

# Joining both the train and vehicle dataframes with the journey data frames
# Creates twio dataframes, onw wth the train as a whoel and one with the individual vehicles

trainjournDf = pd.concat([journeyDf,trainDf], axis=1, sort='false')
vehjournDf = journeyDf.join(vehicleDf, how='right')


#looking at some basic stats from the data that I found intersting

print trainjournDf.loadweigh.isnull().sum(), 'trains have given no loadweigh data:'
no_loadweigh = trainjournDf[trainjournDf.loadweigh.isnull()==True]
no_loadweigh.reset_index(drop=True, inplace=True)
print no_loadweigh.loc[:,('UniqueJourneyId','tiplocIndex')]
print 'This accounts to', (float(no_loadweigh.shape[0])/float(trainjournDf.shape[0])*100.), '% of all legs in the sample'
print

sum_weigh = vehjournDf.reset_index(drop=True)
sum_weigh = sum_weigh.fillna(0.)
tot=0
sums = np.array([])
for i in sum_weigh.index:
    if sum_weigh.sequence.loc[i] == 0:
        sums = np.append(sums,tot)
        tot = 0
        tot = tot + sum_weigh.loadweigh.loc[i]
    else:
        tot = tot + sum_weigh.loadweigh.loc[i]
        
for i in np.arange(10):
    sums = np.append(sums,0)

        
print type(sums), sums.size

        
                           
