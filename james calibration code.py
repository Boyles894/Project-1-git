# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 13:18:14 2018

@author: lb14g16
"""

if modelParameters['aggregation'] == 'train':
    calibrationData = self.journeyDf.join(self.trainDf, how='right')
elif modelParameters['aggregation'] == 'vehicle':
    calibrationData = self.journeyDf.join(self.vehicleDf, how='right')
    calibrationData.set_index('sequence', append=True, inplace=True, drop = False)


