# Leidener Klammersystem

A parser for the "Leidener Klammersystem" which is a notation used in 
archaeology for transcribing inscriptions

Author: Eckhart Arnold <Eckhart.Arnold@badw.de>, 
Bavarian Academy of Sciences and Humanities

## Getting started

- Clone the repo
- Install packages:
  ```
  pip install DHParser
  pip install pandas
  ```
- Run `epi2dio.py` or `lks2epi.py`


To generate parsers:
```
dhparser LKS.ebnf
dhparser dio.ebnf
```

To run tests:
```
python tst_LKS_grammar.py tests_grammar/02_test_lks_passau.ini
python tst_dio_grammar.py tests_grammar/03_test_dio_passau.ini
```

## License

LKS is open source software under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0)

Copyright 2025 Eckhart Arnold <Eckhart.Arnold@badw.de>, 
Bavarian Academy of Sciences and Humanities

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## Status

very first draft
