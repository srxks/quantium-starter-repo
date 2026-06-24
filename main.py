import csv
import pandas as pd

x = open("data/daily_sales_data_0.csv")
y = open("data/daily_sales_data_1.csv")
z = open("data/daily_sales_data_2.csv")
j = open("final.csv", mode="w+", newline="")


a = csv.DictReader(x, delimiter=",")
b = csv.DictReader(y, delimiter=",")
c = csv.DictReader(z, delimiter=",")
d = csv.DictWriter(j, delimiter=",", fieldnames=["sales", "date", "region"])
d.writeheader()

for i in a:
    if i["product"] == "pink morsel":
        h = "$" + str(float(i["price"][1:])*float(i["quantity"]))
        d.writerow({"sales":h, "date":i["date"], "region":i["region"]})

for i in b:
    if i["product"] == "pink morsel":
        h = "$" + str(float(i["price"][1:])*float(i["quantity"]))
        d.writerow({"sales":h, "date":i["date"], "region":i["region"]})

for i in c:
    if i["product"] == "pink morsel":
        h = "$" + str(float(i["price"][1:])*float(i["quantity"]))
        d.writerow({"sales":h, "date":i["date"], "region":i["region"]})
