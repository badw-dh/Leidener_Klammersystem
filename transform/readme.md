# Parsing results

## Broken articles

The file dio_preprocess.csv contains fixes for broken articles.

- search:  A regex that matches broken markup
- replace: The replacement pattern. 
           An empty string removes the matched text.
- cases:   A comma separated list of case numbers.
           This will help to fix the cases directly in T3. 
 

TODO:   
- 80: NBSP im snt
- 192: Allein stehender Doppelpunkt
