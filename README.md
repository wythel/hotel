# Hotel price checker
## Getting started

1. Install [python](https://www.python.org/)
2. Create a virtual environment: `python -m venv run`
3. Activate the venv
4. Install `poetry` by `pip install poetry`
5. Install the requirments `poetry install`

## Get the price for a single hotel and dates
```
python hotel.py --name <HOTEL_NAME> --start-date <START_DATE> --end-date <END_DATE>

CHECK-IN DATE and CHECK-OUT DATE in the format like
8月10日, or 11月11日
```

## Get the list of prices by providing a csv file
```
python htoel.py --from-csv-file input.csv

# check input.csv as example
```

## 跑Pipeline
1. 把branch換成`leo`
2. 修改`input.csv`
3. Commit修改的內容
4. 去Build -> Pipeline找到triggered pipeline
5. Pipeline完成之後按`run script`的job
6. 按右邊的Browse下載Excel檔
