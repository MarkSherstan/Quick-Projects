# Download data from https://www.morningstar.ca/ca/
# Morning star (select stock) -> performance -> Key ratios -> full key ratios data -> export to .csv

# Required packages
import pandas as pd
import numpy as np
import glob

# Exchange rate from Google finance (March 22, 2020)
CAD2USD = 0.691755
USD2CAD = 1/CAD2USD

# Master dataframe for all the data
masterDF = pd.DataFrame()

for file in glob.iglob('data/*.csv'):
    # Set the stock name
    stockName = file.replace('data/','').replace(' Key Ratios.csv','')

    # Read file in data folder and manipulate the dataframe for consitency
    df = pd.read_csv(file, skiprows=[0,1], sep=",", header=0, index_col=0)
    df = df.drop(labels='TTM', axis=1)
    df.columns = range(len(df.columns))
    
    # Pull the data to be analyzed
    netIncome = df.loc['Net Income USD Mil'].str.replace(',', '').astype(float)
    dividends = df.loc['Dividends USD',:].str.replace(',', '').astype(float)
    shares = df.loc['Shares Mil',:].str.replace(',', '').astype(float)
    payoutRatio = df.loc['Payout Ratio % *',:].str.replace(',', '').astype(float)
    returnOnEquity = df.loc['Return on Equity %',:].str.replace(',', '').astype(float)
    revenue = df.loc['Revenue USD Mil',:].str.replace(',', '').astype(float)
    netMargin = df.loc['Net Margin %',:].str.replace(',', '').astype(float)
    opCashFlow = df.loc['Operating Cash Flow USD Mil',:].str.replace(',', '').astype(float)
    longTermDebt = df.loc['Long-Term Debt',:].str.replace(',', '').astype(float)
    earningsPerShare = df.loc['Earnings Per Share USD',:].str.replace(',', '').astype(float)
    currentAssets = df.loc['Total Current Assets',:].str.replace(',', '').astype(float)
    currentLiabilities = df.loc['Total Current Liabilities',:].str.replace(',', '').astype(float)
    bookValuePerShare = df.loc['Book Value Per Share * USD',:].str.replace(',', '').astype(float)
    
    # Calculate a few ratios
    revenue_share = revenue/shares
    opCashFlow_share = opCashFlow/shares
    longTermDebt_share = longTermDebt/shares
    currentRatio = currentAssets/currentLiabilities
    
    # Only log data that is important
    netIncome['ID'] = stockName + '_netIncome'
    dividends['ID'] = stockName + '_dividends'
    shares['ID'] = stockName + '_shares'
    payoutRatio['ID'] = stockName + '_payoutRatio'
    returnOnEquity['ID'] = stockName + '_returnOnEquity'
    revenue['ID'] = stockName + '_revenue'
    opCashFlow['ID'] = stockName + '_opCashFlow'
    longTermDebt['ID'] = stockName + '_longTermDebt'
    netMargin['ID'] = stockName + '_netMargin'
    revenue_share['ID'] = stockName + '_revenue/share'
    opCashFlow_share['ID'] = stockName + '_opCashFlow/share'
    longTermDebt_share['ID'] = stockName + '_longTermDebt/share'
    earningsPerShare['ID'] = stockName + '_earningsPerShare'
    bookValuePerShare['ID'] = stockName + '_bookValuePerShare'
    currentRatio['ID'] = stockName + '_currentRatio'
    
    # Combine this stocks data into a single df and merge with the rest of the data
    objs = [netIncome, dividends, shares, payoutRatio, returnOnEquity, revenue, opCashFlow, longTermDebt, netMargin,
    revenue_share, opCashFlow_share, longTermDebt_share, earningsPerShare, bookValuePerShare, currentRatio]
    
    temp = pd.concat(objs, axis=1, ignore_index=True).T
    masterDF = pd.concat([masterDF, temp])
    
# Save the data to a csv
masterDF.to_csv('stocksMerged.csv')

