# ------------------------------------------------------------------------
#   Last modified: 21 January 2025
#
#   Ranked abundance 
#
#   data --> file.xlsx
#   sheet --> sheet of interest
#   code1 --> name of group1 for the output file
#   code2 --> name of group2 for the output file
#   file_path --> local for the output file
#   file_name --> name of the output file
#
#   python3.1* rank_by_abundance.py file.xlsx sheet code1 code2
#   file_path file_name
#
# ------------------------------------------------------------------------

import sys
import pandas as pd

data = sys.argv[1] #data
sheet = int(sys.argv[2]) #sheet of interest
code1 = sys.argv[3] #name of group1 
code2 = sys.argv[4] #name of group2
file_path = sys.argv[5] #path for output file --> e.g. ../file_path/
file_name = sys.argv[6] #output file --> e.g. output_file.xlsx

#extract data
data = pd.read_excel(data, sheet_name=sheet)

#extract data of interest (see name of variables)
names = data.iloc[:,0]
group1 = data.iloc[:,1:4]
group2 = data.iloc[:,4:7]
group1 = group1.sum(axis=1)
group2 = group2.sum(axis=1)
all = data.iloc[:,1:]
all = all.sum(axis=1)

#put together the data
group1 = pd.concat([names, group1], axis=1)
group2 = pd.concat([names, group2], axis=1)
all = pd.concat([names,all], axis=1)
#sort data by the first column (0)
ranked_group1 = group1.sort_values(by=0)
ranked_group2 = group2.sort_values(by=0)
ranked_all = all.sort_values(by=0)
#reverse list
ranked_group1 = ranked_group1.iloc[::-1]
ranked_group2 = ranked_group2.iloc[::-1]
ranked_all = ranked_all.iloc[::-1]
#reset the index and not transform the old index into a new column
ranked_group1 = ranked_group1.reset_index(drop=True) 
ranked_group2 = ranked_group2.reset_index(drop=True)
ranked_all = ranked_all.reset_index(drop=True)

#put together all data of interest into a dataframe
ranked_abundance = pd.concat([ranked_group1,ranked_group2,ranked_all], axis=1, ignore_index=True)
ranked_abundance.columns = ['Genes', code1, 'Genes', code2, 'Genes', 'All samples']

#save the data into excel file
with pd.ExcelWriter(file_path+file_name) as writer:
    ranked_abundance.to_excel(writer,sheet_name='ranked abundance', index=False)
