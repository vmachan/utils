#
# Convert delimited output from Oracle SQLPLUS (or any other program) to Oracle SQLDeveloper's Fixed format
# At the time of writing this there was no such tool/utility available so wrote this script
# Need to enhance to accept input file as a parameter and generate corresponding output file name
#

import os
import numpy as np
import pandas as pd
import sklearn as sk
import csv

os.listdir()

h1b_df = pd.read_csv('test_h1b_data.txt', sep='\t', dtype=object, quoting=csv.QUOTE_ALL)
h1b_df.describe()
h1b_df.info()
h1b_df.head()

# replace NaN values with 0
h1b_df.fillna(0, inplace=True)

# Replace NaN values with zeroes
h1b_df.fillna(0)

# Now left-justify ALL the columns in data frame, with width of 28
out_df = h1b_df.applymap(lambda x: str(x)[:28].ljust(28))
out_df

# Now change the header row to be left-justified with 28 column width
out_df.columns.values
# convert to list so that it can be used to change the header 
list(pd.Series(out_df.columns.values).apply(lambda x: x.ljust(28)))
out_df.columns = list(pd.Series(out_df.columns.values).apply(lambda x: x.ljust(28)))
out_df.columns.values

# Write to output delimited file
# Note that the delimited will need to be removed by an external/another script 
# since this function does not take null column separator 
out_df.to_csv("h1b_out.txt", sep='|', doublequote=True, quoting=csv.QUOTE_ALL, index=False)

