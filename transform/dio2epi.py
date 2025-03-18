#%%
#
# Transform DI-Passau-Band to test case
#

import pandas as pd
import xml.etree.ElementTree as ET
import LKSParser

#%% Extract transcriptions

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

# Add case numbers
df['case'] = range(1, len(df) + 1)
df = df.explode('text')
df['lno'] = df.groupby('case').cumcount() + 1


#%% Parse all

df['error'] = ""
df['parsed'] = ""

for idx, row in df.iterrows():
    try:
        source = row['text']
        result, errors = LKSParser.compile_src("\n" + source)
        df.loc[idx,'parsed'] = result.as_xml()
    except Exception as e:
        df.loc[idx, 'error'] = str(e)


#%% Save
tests = ""
for idx, row in df.iterrows():
    tests = tests + "\n" + "C" + str(row['case']) + 'L' + str(row['lno']) + ": " + str(row['text'])

with open("tests_grammar/02_test_di_passau.ini", "w", encoding="utf-8") as file:
    file.write("[match:inscription]\n" + tests)
