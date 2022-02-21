# -*- coding: UTF-8 -*-
import pandas as pd
import tabula


# Read a PDF File
dfs = tabula.read_pdf("Untitled.pdf", pages='1-2', lattice=True, pandas_options={'header': None})
# Get DataFrame with data to process
dfs[3].drop(labels=[0,1,2], axis=0, inplace=True)
df_data = dfs[3]


# Get df with name of file
df_name = dfs[5]


print(df_data, end='\n', sep='\n')
# print(df_data, end='\n', sep='\n')
print(df_data.columns)
# print(len(dfs))
# print(dfs[3], dfs[5], end='\n', sep='\n')
# dfs[1].to_csv('out.csv', sep=',', encoding='utf-8', index=False)


# df = tabula.read_pdf("Untitled.pdf", pages='all')[0:1]
# df.to_csv('out.csv', sep=',', encoding='utf-8')

# Read data from the csv file in the current directory
# df = pd.read_csv('Untitled_page0.txt', sep=' ')
#
# print(df)