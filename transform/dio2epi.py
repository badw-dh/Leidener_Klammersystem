#%%
#
# Transform DI-Passau-Band to test case
#

import pandas as pd
import xml.etree.ElementTree as ET
import LKSParser

#%%

df = pd.read_csv("data/dio_inschriften.csv", delimiter = ';')

def extract_lno_text(xml_string):
    lines = []
    root = ET.fromstring(xml_string)
    for elem in root.findall(".//lno"):
        elm_xml = ET.tostring(elem, encoding="unicode", method="xml")
        elm_xml = elm_xml.replace(f"<lno>", "").replace(f"</lno>", "")  # Remove <lno> tags
        lines.append(elm_xml)
    return lines

df['text'] = df['content'].apply(extract_lno_text)
df = df.drop(columns=['content_clean', 'content'])
df['case'] = range(1, len(df) + 1)
df = df.explode('text')
df['lno'] = df.groupby('case').cumcount() + 1


#%%

df['error'] = ""
df['parsed'] = ""

for idx, row in df.iterrows():
    try:
        source = row['text']
        result, errors = LKSParser.compile_src("\n" + source)
        df.loc[idx,'parsed'] = result.as_xml()
    except Exception as e:
        df.loc[idx, 'error'] = str(e)


#%%
tests = ""
for idx, row in df.iterrows():
    #test = "C" + str(row['case']) + 'L' + str(row['lno']) + ' "' + row['text'] + '" '
    test = "C" + str(row['case']) + 'L' + str(row['lno']) + ": " + str(row['text'])
    tests = tests + "\n" + test

#%%
with open("tests_grammar/02_test_di_passau.ini", "w", encoding="utf-8") as file:
    file.write("[match:di-passau]\n" + tests)