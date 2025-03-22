#%%
#
# Transform DIO data from the T3 database
#
# Step 1: Preprocess text.
#         Replaces broken markup,  see dio_preprocess.csv
# Step 2: Transform the data using the dio.ebnf grammar.
#         The script shows a summary statistic of how many files were well-formed.
#
# For developing the grammar, this script generates the test file
# 03_test_dio_sco_passau.ini which contains the content as ist comes from the T3 database.
# It includes structural markup (sco, sec, par tags...).
#   This file can be used to develop the dio.ebnf.
#
# The data is XML, that means angle brackets in the inscriptions
# are represented with named entities (&lt; &gt;).
#
#

import pandas as pd
import dioParser
from tqdm import tqdm

import importlib
importlib.reload(dioParser)

#%% Load transcriptions

filename = 'dio_inschriften_all'

df = pd.read_csv("data/input/" + filename + ".csv", delimiter = ';')
df['case'] = range(1, len(df) + 1)

#%% Preprocess
regs = pd.read_csv("data/dio_preprocess.csv", delimiter = ';', keep_default_na=False)
for idx, row in regs.iterrows():
    df['content'] =  df['content'].str.replace(row['search'], row['replace'], regex=True)

#%% Save test cases for dio sco

tests = ""
for idx, row in df.iterrows():
    inscription = str(row['content']).strip()
    tests += f"\nC{str(row['case'])}: "
    tests += '"""' + inscription + '"""'

with open("tests_grammar/" + filename + ".ini", "w", encoding="utf-8") as file:
    file.write("[match:sco]\n" + tests)

#%% Build parser

dioParser.recompile_grammar("dio.ebnf", "dioParser.py", force=True)

#%% Parse all dio sco

df['error'] = ""
df['parsed'] = ""

for idx, row in tqdm(df.iterrows()):
    try:
        source = row['content'].strip()
        result, errors = dioParser.compile_snippet(source)
        strings = ["letters", "terminator", "space"]
        # TODO: do we need to list all those tags?
        inline =  ["lno","lin","snt","snr","wtr","abr","rasure","del","cpl","add","insec","lig","b","strong","em","chr","sup","nl","appalpha","appnum"]
        df.loc[idx,'parsed'] = result.as_xml(string_tags= strings, inline_tags = inline, indentation=2)
    except Exception as e:
        df.loc[idx, 'error'] = str(e)

# How many are well-formed?
df['ok'] = df['parsed'].str.startswith("<sco>")
print(df['ok'].value_counts())

#%% Save result

df.to_csv("data/output/" + filename + ".csv")