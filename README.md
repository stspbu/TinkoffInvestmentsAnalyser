# Tinkoff Investments Analyser
A tool for analysing Tinkoff investments portfolio. 
The tool takes information through [OpenAPI](https://tinkoffcreditsystems.github.io/invest-openapi/).

## Getting started
0. The tool requires Python 3 to run.
1. Install the required dependencies:

    ```shell script
    pip3 install -r requirements.txt
    ```
2. Create _settings.json_ based on 
[_conf/settings.json.example_](https://github.com/stspbu/TinkoffInvestmentsAnalyser/blob/master/conf/settings.json.example) 
and save it in the 
[same directory](https://github.com/stspbu/TinkoffInvestmentsAnalyser/tree/master/conf). 
   
## How to use
Run the main script as follows:
```shell script
python3 main.py
```
