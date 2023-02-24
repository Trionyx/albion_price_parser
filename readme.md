# Albion price parser for albiononline2d.com

Script parses prices from albiononline2d.com and evaluates price spread between main and production cities.
Total 2000+ rows of data

Data saves to Google Sheets for later analysis.

Can be easily changed to any DB or tool because of Pandas.

## Usage
1. Install requirements.txt
2. Setup Google Sheets API using this guide: https://youtube.com/watch?v=aruInGd-m40
3. Create confing.py from config.py.example and fill it with your data
2. Run `python3 main.py`
3. Wait for script to finish
4. Check Google Sheets for results

Note: gs_credentials.json is not included in repo. You should create it yourself using guide above.

## Some stats
Total 2000+ rows of data

Average run time: 32 minutes on weak laptop and internet connection


# roadmap

1. Some subcats should be able to mark as `useless` such as: https://albiononline2d.com/en/item/cat/armor/subcat/cape
2. Add item weight parameter to data
3. Evaluate potential profit on character inventory weight
