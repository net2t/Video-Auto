import csv

fname = "stories.csv"
rows = []
with open(fname, "r", encoding="utf-8", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)
    rows.append(header)
    for i, r in enumerate(reader):
        row_num = i + 2 # Header is row 1
        if row_num in [24, 25, 26]:
            r[0] = "Pending"
            # Clear all columns from Gen_Title (col 4) onwards
            for j in range(4, len(r)):
                r[j] = ""
        rows.append(r)

with open(fname, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("Fixed stories.csv rows 24, 25, 26 back to Pending.")
