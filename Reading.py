import csv
import pandas as pd
from numpy.core.numeric import indices

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
            if(cnt != 0):
                avgOccurrence = sum / (cnt * numOtus)
            else:
                avgOccurrence = 0
            new.append(avgOccurrence)

            sum = 0
            cnt = 0
            sum += row[ind]
            if(row[ind] != 0):
                cnt += 1
        lastSpec = row[2]
        
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
            if(cnt != 0):
                avgOccurrence = sum / (cnt * numOtus)
            else:
                avgOccurrence = 0
            new.append(avgOccurrence)

            sum = 0
            cnt = 0
            sum += row[ind]
            cnt += 1
        lastSpec = row[2]
        
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

def findTopTen(rows):
    averages = []
    for row in rows:
        sum = 0
        for number in row:
            sum += number
        averages.append(sum / len(row))
    
    indices = sorted(range(len(averages)), key =lambda i: averages[i])[-10:]
    indices.reverse()
    
    top_rows = []
    for index in indices:
        top_rows.append(rows[index])
        
    return indices, top_rows

def edit(df):
    del df['label']
    del df["Group"]
    df = df.loc[df["Category"] != "water"]
    df = df.loc[df["Category"] != "soil"]
    df = df.loc[df["Category"] != "moss"] 
    return df

def rowNames(indices, labels):
    rows = []
    for index in indices:
        rows.append(labels[index + 3])
        
    return rows

def main():
    path = r"C:\Users\sofib\Documents\desmogs_data.csv"
    df = pd.read_csv(path)
    df = edit(df)
    columns = columnNames(df)
    occurrence = []
    
    for ind in range(4, 24):
        new = noZeros(df, ind)
        occurrence.append(new)
    
    result = findTopTen(occurrence)
    indices = result[0]
    final = result[1]
    rows = rowNames(indices, df.columns)
    
    print(columns)
    print(rows)
    for i in range(0,10):
        print(indices[i])
    for i in range(0,10):
        print(final[i])
        
main()
