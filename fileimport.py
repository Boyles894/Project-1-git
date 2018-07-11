import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def indexDataFrame(df, indexColumns, retainCols=False):
    if retainCols == True:
        df.set_index(indexColumns, drop=False, inplace=True)
    else:
        df.set_index(indexColumns, drop=True, inplace=True)

if __name__ == '__main__':

    filepath = 'C:\\Users\\lwb1u18\Internship\Project 1\datafiles\cddb.h5'

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

print ((trainjournDf.loadweigh.isnull().sum()), ('trains have given no loadweigh data:'))
no_loadweigh = trainjournDf[trainjournDf.loadweigh.isnull()==True]
no_loadweigh.reset_index(drop=True, inplace=True)
print (no_loadweigh.loc[:,('UniqueJourneyId','tiplocIndex')])
print ('This accounts to', ((float(no_loadweigh.shape[0])/float(trainjournDf.shape[0])*100.)), '% of all legs in the sample')
print ()


traintime = trainjournDf.set_index('Hour', drop=False)
traintime = (traintime.index.value_counts())
traintime.index = traintime.index.astype(int)
traintime = traintime.sort_index(axis=0, ascending=True)
traintime.plot()
plt.xlabel('Time (24-hour)')
plt.ylabel('No. of Trains')
plt.ylim(5,20)
plt.title('No. of trains travelling throughout the day')
