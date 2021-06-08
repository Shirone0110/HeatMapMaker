import csv
import pandas as pd

#calculates averages for one row not including zeros
def noZeros(df, ind):
    sum = 0
    cnt = 0
    new = []
    lastSpec = df.at[0, "Category"]
    numOtus = df.at[0, "numOtus"]
    
    for row in df.itertuples():
        if(row[2] == lastSpec):
            sum += row[ind]
            if(row[ind] != 0):
                cnt += 1
        else:
            avgOcurrence = sum / (cnt * numOtus)
            new.append(avgOcurrence)

            sum = 0
            cnt = 0
            sum += row[ind]
            if(row[ind] != 0):
                cnt += 1
        lastSpec = row[2]
        genus = row[3]
        
    return new

#calculates averages for one row including zeros
def inclZeros(df, ind):
    sum = 0
    cnt = 0
    new = []
    lastSpec = df.at[0, "Category"]
    numOtus = df.at[0, "numOtus"]
    
    for row in df.itertuples():
        if(row[2] == lastSpec):
            sum += row[ind]
            cnt += 1
        else:
            avgOcurrence = sum / (cnt * numOtus)
            new.append(avgOcurrence)

            sum = 0
            cnt = 0
            sum += row[ind]
            cnt += 1
        lastSpec = row[2]
        genus = row[3]
        
    return new
    
def columnNames(df):
    columns = []
    lastSpec = df.at[0, "Category"]
    genus = df.at[0, "Sub"]
    
    for row in df.itertuples():
        if row[2] != lastSpec:
            columns.append(genus[0] + ". " + lastSpec)
            lastSpec = row[2]
            genus = row[3]
            
    return columns

def edit(df):
    del df['label']
    del df["Group"]
    df = df.loc[df["Category"] != "water"]
    df = df.loc[df["Category"] != "soil"]
    df = df.loc[df["Category"] != "moss"] 
    return df

def main():
    path = r"C:\Users\sofib\Documents\desmogs_data.csv"
    df = pd.read_csv(path)
    df = edit(df)
    columns = columnNames(df)
    occurrence = []
    ind = 4
    
    for ind in range(ind, 10):
        new = noZeros(df, ind)
        occurrence.append(new)
        ind += 1
    
    print(columns)
    for row in occurrence:
        print(row)
        
main()