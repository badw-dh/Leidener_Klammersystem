#%%
#
# Transform DIO data
#
# Step 1: Preprocess text.
#         Replaces broken markup,  see dio_preprocess.csv
# Step 2: Transform the data using the dio.ebnf grammar.
#         The script shows a summary statistic of how many files were well-formed.
#
# For developing the grammar, this script generates two test files
# - 03_test_dio_sco_passau.ini contains the content as ist comes from the T3 database
#   It includes structural markup (sco, sec, par tags...)
# - 02_test_di_passau.ini contains only inscription text inside lno tags.
#   This file can be used to develop the LKS.ebnf.
#
# The data is XML, that means angle brackets in the inscriptions
# are represented with named entities (&lt; &gt;).
#
#

import pandas as pd
import xml.etree.ElementTree as ET
import LKSParser
import dioParser

import importlib
importlib.reload(dioParser)

#%% Load transcriptions

df = pd.read_csv("data/dio_inschriften.csv", delimiter = ';')
df['case'] = range(1, len(df) + 1)

#%% Preprocess
regs = pd.read_csv("data/dio_preprocess.csv", delimiter = ';', keep_default_na=False)
for idx, row in regs.iterrows():
    print(row['search'])
    df['content'] =  df['content'].str.replace(row['search'], row['replace'], regex=True)

#%% Parse all dio sco

df['error'] = ""
df['parsed'] = ""

for idx, row in df.iterrows():
    try:
        source = row['content'].strip()
        result, errors = dioParser.compile_src("\n" + source)
        df.loc[idx,'parsed'] = result.as_xml()
    except Exception as e:
        df.loc[idx, 'error'] = str(e)

# How many are well-formed?
df['ok'] = df['parsed'].str.startswith("<sco>")
print(df['ok'].value_counts())

#%% Save test cases for dio sco

tests = ""
for idx, row in df.iterrows():
    inscription = str(row['content']).strip()
    tests += f"\nC{str(row['case'])}: "
    tests += '"""' + inscription + '"""'

with open("tests_grammar/03_test_dio_sco_passau.ini", "w", encoding="utf-8") as file:
    file.write("[match:sco]\n" + tests)

#%% Extract lines
def extract_lno_text(xml_string):
    lines = []
    root = ET.fromstring(xml_string)
    for elem in root.findall(".//lno"):
        elm_xml = ET.tostring(elem, encoding="unicode", method="xml")
        elm_xml = elm_xml.replace(f"<lno>", "").replace(f"</lno>", "")  # Remove <lno> tags
        lines.append(elm_xml)
    return lines

df_lines = df.copy()
df_lines['text'] = df_lines['content'].apply(extract_lno_text)
df_lines = df_lines.drop(columns=['content_clean', 'content'])

# Add case numbers
df_lines = df_lines.explode('text')
df_lines['lno'] = df_lines.groupby('case').cumcount() + 1

#%% Parse all lines

df_lines['error'] = ""
df_lines['parsed'] = ""

for idx, row in df_lines.iterrows():
    try:
        source = row['text'].strip()
        result, errors = LKSParser.compile_src("\n" + source)
        df_lines.loc[idx,'parsed'] = result.as_xml()
    except Exception as e:
        df_lines.loc[idx, 'error'] = str(e)

# How many are well-formed?
df_lines['ok'] = df_lines['parsed'].str.startswith("<inscription>")
print(df_lines['ok'].value_counts())

#%% Save lines test file

tests = ""
for idx, row in df_lines.iterrows():
    inscription = str(row['text']).strip()
    tests += f"\nC{str(row['case'])}L{str(row['lno'])}: "
    tests += '"""' + inscription + '"""'

with open("tests_grammar/02_test_di_passau.ini", "w", encoding="utf-8") as file:
    file.write("[match:inscription]\n" + tests)

