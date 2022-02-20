# -*- coding: UTF-8 -*-
import pandas as pd
import tabula


# Read a PDF File
dfs = tabula.read_pdf("Untitled.pdf", pages='1-2', lattice=True)

print(len(dfs))
print(dfs[5])
# dfs[1].to_csv('out.csv', sep=',', encoding='utf-8', index=False)
# for df in dfs:
    # print(df, end='\n', sep='\n')
    # df.to_csv(f'{df}.csv', sep=',', encoding='utf-8')
# df = tabula.read_pdf("Untitled.pdf", pages='all')[0]
# convert PDF into CSV
# tabula.convert_into("Untitled.pdf", "Untitled.csv", output_format="csv", pages='1-3')
# print(df)

# df = tabula.read_pdf("Untitled.pdf", pages='all')[0:1]
# df.to_csv('out.csv', sep=',', encoding='utf-8')

# Read data from the csv file in the current directory
# df = pd.read_csv('Untitled_page0.txt', sep=' ')
#
# print(df)