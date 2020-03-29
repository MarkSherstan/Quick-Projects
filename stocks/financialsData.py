# Download data from https://www.morningstar.ca/ca/
# Morning star (select stock) -> financials -> quote -> all financials data -> balance sheet -> export to .csv

# Required packages
import pandas as pd
import numpy as np
import glob

# Master dataframe for all the data
masterDF = pd.DataFrame()

# Loop through the data directory looking only at .csv files
for file in glob.iglob('financialsData/*.csv'):
    # Set the stock name
    stockName = file.replace('financialsData/','').replace(' Balance Sheet.csv','')

    # Read current file in data folder and manipulate the dataframe for consistency
    df = pd.read_csv(file, skiprows=[0], sep=",", header=0, index_col=0)
    df.columns = range(len(df.columns))

    # Pull the data to be analyzed
    try:
        totalCash = df.loc['Total cash'].astype(float).astype(float)
    except:
        totalCash = pd.Series(0)
            
    try:
        shortTermDebt = df.loc['Short-term debt',:].astype(float)
    except:
        shortTermDebt = pd.Series(0)
        
    try:
        longTermDebt = df.loc['Long-term debt',:].astype(float)
    except:
        longTermDebt = pd.Series(0)
        
    # Only log data that is important
    totalCash['ID'] = 'totalCash' + stockName
    shortTermDebt['ID'] = 'shortTermDebt' + stockName
    longTermDebt['ID'] = 'longTermDebt' + stockName
      
    # Combine this stocks data into a single df and merge with the rest of the data
    objs = [totalCash, shortTermDebt, longTermDebt]
    
    temp = pd.concat(objs, axis=1, ignore_index=True, sort=True).T
    masterDF = pd.concat([masterDF, temp])
    
# Save the data to a csv
masterDF.to_csv('financialDataMerged.csv')

