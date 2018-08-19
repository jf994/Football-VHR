import csv

def get_opt():
    with open('options.csv', 'r') as f:
        reader = csv.reader(f)
        array = list(reader)[0]

        return array

