# Parsing results

## Broken articles

The file dio_preprocess.csv contains fixes for broken articles.

- search:  A regex that matches broken markup
- replace: The replacement pattern. 
           An empty string removes the matched text.
- cases:   A comma separated list of case numbers.
           This will help to fix the cases directly in T3. 
 

TODO:   
- 269: Überklammerung
- 324: Remove empty sup-tag (to avoid empty appnum)
- 328: Check footnote detection; footnote 5 in sup-tag online but not recognized in preprocessing
