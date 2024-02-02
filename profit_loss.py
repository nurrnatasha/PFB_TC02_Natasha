# pulling data from csv file
from pathlib import Path
import csv

def get_profit_deficit(deficit_record):
    """ Returns the profit deficit amount from the deficit record tuple for sorting purposes. """
    return deficit_record[0]

def processpaldata():
    """ create a file path to csv file """
    fp = Path.cwd() / "csv_reports" / "Profits_and_Loss.csv"

    # initialize variables
    prevpl = 0
    maxchange = 0
    maxday = None
    maxloss = 0
    maxlossday = 0
    increases = True
    decreases = True
    all_losses = []
    count = 0

    # read the csv file
    with fp.open(mode="r", encoding="UTF-8", newline="") as file:
        lists = csv.reader(file)
        next(lists)  # skip header

        for alist in lists:
            if count <= 0:
                count += 1
                continue
            pl = int(alist[4])  # convert into int
            currentchange = pl - prevpl # find change in profit and loss
            if pl > prevpl:
                decreases = False
            if pl < prevpl:
                increases = False
                all_losses.append((abs(currentchange), alist[0])) 
                if maxloss <= 0 or maxloss < abs(currentchange):
                    maxloss = abs(currentchange)
                    maxlossday = alist[0]
            if abs(currentchange) > abs(maxchange):
                maxchange = currentchange
                maxday = alist[0]
            prevpl = pl

    # output file path
    fp = Path.cwd() / "summary_report.txt"
    fp.touch()
    with fp.open(mode="a", encoding="UTF-8") as file:

        # writing the net profit surplus and deficit
        if increases:
            file.write( f"[NET PROFIT SURPLUS] PROFIT ON EACH DAY IS HIGHER THAN THE PREVIOUS DAY")
        elif decreases:
            file.write( f"[NET PROFIT DEFICIT] PROFIT ON EACH DAY IS LOWER THAN THE PREVIOUS DAY")
        else:
            for loss in all_losses:
                file.write(f"\n[NET PROFIT DEFICIT] DAY: {loss[1]}, AMOUNT: SGD {loss[0]}")

        # find the top 3 profit deficits
        all_losses.sort(key=get_profit_deficit, reverse=True)  # Sort by deficit amount, descending
        top_deficits = all_losses[:3]  # Take the top 3 elements

        # write the top 3 profit deficits to the file
        deficit_titles = ["HIGHEST NET PROFIT DEFICIT", "2ND HIGHEST NET PROFIT DEFICIT", "3RD HIGHEST NET PROFIT DEFICIT"]
        for i, (amount, day) in enumerate(top_deficits):
            title = deficit_titles[i] if i < len(deficit_titles) else f"{i+1}TH HIGHEST NET PROFIT DEFICIT"
            file.write (f"\n[{title}] DAY: {day}, AMOUNT: SGD {amount}")