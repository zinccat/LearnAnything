# open a csv file, check the first column for unprobed
# if unprobed, write the line to a new csv file

import csv

count = 60002

with open("data/60002_80000.csv", "r") as csvfile:
    reader = list(csv.reader(csvfile, delimiter=","))
    with open("unprobed.csv", "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        length = len(reader)
        cnt = 0
        while cnt < length:
            row = reader[cnt]
            if row[0] != str(count):
                print(row[0], count)
                # break
                writer.writerow([count])
            else:
                cnt += 1
            count += 4
            if count > 80000:
                break
