# Download data from https://www.morningstar.ca/ca/
# Morning star (select stock) -> performance -> key ratios -> full key ratios data -> export to .csv

# Required packages
import pandas as pd
import numpy as np
import glob

# Exchange rate from Google finance (March 22, 2020)
CAD2USD = 0.691755
USD2CAD = 1/CAD2USD

# Master dataframe for all the data
masterDF = pd.DataFrame()

# Loop through the data directory looking only at .csv files
for file in glob.iglob('data/*.csv'):
    # Set the stock name
    stockName = file.replace('data/','').replace(' Key Ratios.csv','')

    # Read current file in data folder and manipulate the dataframe for consistency
    df = pd.read_csv(file, skiprows=[0,1], sep=",", header=0, index_col=0)
    df = df.drop(labels='TTM', axis=1)
    df.columns = range(len(df.columns))
    
    # Pull the data to be analyzed (always in USD)
    try:
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
    except:
        netIncome = df.loc['Net Income CAD Mil'].str.replace(',', '').astype(float) * CAD2USD
        dividends = df.loc['Dividends CAD',:].str.replace(',', '').astype(float) * CAD2USD
        shares = df.loc['Shares Mil',:].str.replace(',', '').astype(float)
        payoutRatio = df.loc['Payout Ratio % *',:].str.replace(',', '').astype(float)
        returnOnEquity = df.loc['Return on Equity %',:].str.replace(',', '').astype(float)
        revenue = df.loc['Revenue CAD Mil',:].str.replace(',', '').astype(float) * CAD2USD
        netMargin = df.loc['Net Margin %',:].str.replace(',', '').astype(float)
        opCashFlow = df.loc['Operating Cash Flow CAD Mil',:].str.replace(',', '').astype(float) * CAD2USD
        longTermDebt = df.loc['Long-Term Debt',:].str.replace(',', '').astype(float) * CAD2USD
        earningsPerShare = df.loc['Earnings Per Share CAD',:].str.replace(',', '').astype(float) * CAD2USD
        currentAssets = df.loc['Total Current Assets',:].str.replace(',', '').astype(float) * CAD2USD
        currentLiabilities = df.loc['Total Current Liabilities',:].str.replace(',', '').astype(float) * CAD2USD
        bookValuePerShare = df.loc['Book Value Per Share * CAD',:].str.replace(',', '').astype(float) * CAD2USD

    # Calculate a few ratios
    revenue_share = revenue/shares
    opCashFlow_share = opCashFlow/shares
    longTermDebt_share = longTermDebt/shares
    currentRatio = currentAssets/currentLiabilities
    
    # Only log data that is important
    netIncome['ID'] = 'netIncome' + stockName
    dividends['ID'] = 'dividends' + stockName
    shares['ID'] = 'shares' + stockName
    payoutRatio['ID'] = 'payoutRatio' + stockName
    returnOnEquity['ID'] = 'returnOnEquity' + stockName
    revenue['ID'] = 'revenue' + stockName
    opCashFlow['ID'] = 'opCashFlow' + stockName
    longTermDebt['ID'] = 'longTermDebt' + stockName
    netMargin['ID'] = 'netMargin' + stockName
    revenue_share['ID'] = 'revenue/share' + stockName
    opCashFlow_share['ID'] = 'opCashFlow/share' + stockName
    longTermDebt_share['ID'] = 'longTermDebt/share' + stockName
    earningsPerShare['ID'] = 'earningsPerShare' + stockName
    bookValuePerShare['ID'] = 'bookValuePerShare' + stockName
    currentRatio['ID'] = 'currentRatio' + stockName
    
    # Combine this stocks data into a single df and merge with the rest of the data
    objs = [netIncome, dividends, shares, payoutRatio, returnOnEquity, revenue, opCashFlow, longTermDebt, netMargin,
    revenue_share, opCashFlow_share, longTermDebt_share, earningsPerShare, bookValuePerShare, currentRatio]
    
    temp = pd.concat(objs, axis=1, ignore_index=True).T
    masterDF = pd.concat([masterDF, temp])
    
# Save the data to a csv
masterDF.to_csv('stocksMerged.csv')
