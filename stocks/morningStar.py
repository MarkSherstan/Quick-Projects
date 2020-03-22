import pandas as pd
import numpy as np
import glob

# Exchange rate from Google finance
USD2CAD = 1

# Master list for all the data
dataList = []

for file in glob.iglob('data/*.csv'):
    # Set stock name and create a dictionary
    stockName = file.replace('data/','').replace(' Key Ratios.csv','')

    # Read file in data folder
    df = pd.read_csv(file, skiprows=[0,1], sep=",", header=0, index_col=0)

    # Pull the data to be analyzed
    netIncome = df.loc['Net Income USD Mil'].str.replace(',', '').astype(float)
    dividends = df.loc['Dividends USD',:].str.replace(',', '').astype(float)
    shares = df.loc['Shares Mil',:].str.replace(',', '').astype(float)
    payoutRatio = df.loc['Payout Ratio % *',:].str.replace(',', '').astype(float)
    returnOnInvestment = df.loc['Return on Equity %',:].str.replace(',', '').astype(float)
    revenue = df.loc['Revenue USD Mil',:].str.replace(',', '').astype(float)
    netMargin = df.loc['Net Margin %',:].str.replace(',', '').astype(float)
    opCashFlow = df.loc['Operating Cash Flow USD Mil',:].str.replace(',', '').astype(float)
    longTermDebt = df.loc['Long-Term Debt',:].str.replace(',', '').astype(float)
    earningsPerShare = df.loc['Earnings Per Share USD',:].str.replace(',', '').astype(float)
    currentAssets = df.loc['Total Current Assets',:].str.replace(',', '').astype(float)
    currentLiabilities = df.loc['Total Current Liabilities',:].str.replace(',', '').astype(float)

    try:
        bookValuePerShare = df.loc['Book Value Per Share * CAD',:].str.replace(',', '').astype(float) * USD2CAD
    except:
        bookValuePerShare = df.loc['Book Value Per Share * USD',:].str.replace(',', '').astype(float)

    # Calculate a few ratios
    revenue_share = revenue/shares
    opCashFlow_share = opCashFlow/shares
    longTermDebt_share = (longTermDebt/shares)
    currentRatio = (currentAssets/currentLiabilities).tolist().insert(0,stockName)

    
    
    
# dictRow = {}
# .tolist() #.to_numpy
# dictRow['currentRatio'] = (currentAssets/currentLiabilities).tolist().insert(0,stockName)


#    2010-09  2011-09  2012-09  2013-09  2014-09  2015-09  2016-09  2017-09  2018-09  2019-09


#    print(longTermDebt_share)
  
#masterDF = pd.DataFrame(dataList).transpose()
#
#print(masterDF)
#masterDF.to_csv('Test.csv')

