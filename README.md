# Demanz © 2021 Allen D. Montgomery
I hereby grant permission to freely distribute this software and associated files, without modification.

A tool for Demand Forecasting

Before running the program, you should have two csv files, which can be created in Excel.

One is the sales history, and contains the fields, ‘product’, and ‘sold’. If this is six weeks of weekly sales totals, each product would have six rows, each with the amount sold for that week.

The other csv file is the current inventory, with the fields, ‘product’ and ‘current’. Each product in this one should have only one row.

Sample files are available for download at https://github.com/vegebond/Demanz

First you enter the number of days in each period. For weekly sales, enter 7.

The program will calculate the median sales for each product.

Your next entry, the forecast multiplier, is multiplied by this median to allow for variance. A multiplier of 1.15 would increase your forecast by 15%.

The forecast increment is then added to create the adjusted forecast. Let’s say you expect to sell 2, but a person might conceivably buy 10 all at once. The multiplier doesn’t help here, but incrementing the forecast by 10 would.

You now enter three dates, the count date, the delivery date, and the next delivery date.

The next step is to select the file containing your sales history, and the one containing the current inventory.

In order to forecast sales for a given product, that product must appear in both of the input files. An orphan is a product that appears in only one file. You may ignore them if you choose, but they will not be included in the output.

The output is a csv file containing the following fields:

1. product
2. median
3. adjusted (median * multiplier + increment)
4. sales1 – projected sales between the count and the first delivery
5. balance – projected inventory just before the first delivery. A negative number indicates that you are projected to run out of this item.
6. sales2 – projected sales after the first delivery, but before the second.
7. Purchase – recommended purchase quantity (sales2 – max(balance, 0))

