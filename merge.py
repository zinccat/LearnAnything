import csv

# Open the first csv file
with open("merged_file.csv", "r") as f1:
    reader1 = csv.reader(f1)
    data1 = [row for row in reader1]

# Open the second csv file
with open("data/unprobed.csv", "r") as f2:
    reader2 = csv.reader(f2)
    data2 = [row for row in reader2]

merged_data = []

# Merge the two csv files
i = 0
j = 0
while i < len(data1) and j < len(data2):
    if data1[i][0] == data2[j][0]:
        merged_data.append(data1[i])
        i += 1
        j += 1
    elif data1[i][0] < data2[j][0]:
        merged_data.append(data1[i])
        i += 1
    else:
        merged_data.append(data2[j])
        j += 1

# Add any remaining rows from the first csv file
while i < len(data1):
    merged_data.append(data1[i])
    i += 1

# Add any remaining rows from the second csv file
while j < len(data2):
    merged_data.append(data2[j])
    j += 1

# Write the merged data to a new csv file
with open("merged_file.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(merged_data)
