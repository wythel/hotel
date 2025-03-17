# Hotel price checker
## Getting started

1. Install [python](https://www.python.org/)
2. Create a virtual environment: `python -m venv run`
3. Activate the venv
4. Install `poetry` by `pip install poetry`
5. Install the requirments `poetry install`

## Get the price for a single hotel and dates
```
python hotel.py --name <HOTEL_NAME> --check-in <CHECKIN_DATE> --check-out <CHECKOUT_DATE>

CHECK-IN DATE and CHECK-OUT DATE in the format like
8月10日, or 11月11日
```

## Get the list of prices by providing a csv file
```
python htoel.py --from-csv-file input.csv

# check input.csv as example
```
