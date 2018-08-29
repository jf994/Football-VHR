import csv


def get_crops():
    with open('crops_value.csv', 'r') as f:
        reader = csv.reader(f)
        w, h = 4, 3
        array = [[0 for x in range(w)]for y in range(h)]
        for n, row in enumerate(reader):
            if n == 0:
                y_min = row[0]
                y_max = row[1]
            else:
                print(n)
                array[n-1][0] = int(y_min)
                array[n-1][1] = int(y_max)
                array[n-1][2] = int(row[0])
                array[n-1][3] = int(row[1])

        return array
