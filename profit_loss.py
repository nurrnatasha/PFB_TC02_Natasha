from pathlib import Path
import csv

def get_profit_deficit(deficit_record):
    """ Returns the profit deficit amount from the deficit record tuple for sorting purposes. """
    return deficit_record[0]

def processpaldata():
    # create a file path to csv file
    fp = Path.cwd() / "csv_reports" / "Profits_and_Loss.csv"

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
            currentchange = pl - prevpl
            if pl > prevpl:
                decreases = False
            if pl < prevpl:
                increases = False
                all_losses.append((abs(currentchange), alist[0]))  # Note: switched order to (amount, day) for sorting
                if maxloss <= 0 or maxloss < abs(currentchange):
                    maxloss = abs(currentchange)
                    maxlossday = alist[0]
            if abs(currentchange) > abs(maxchange):
                maxchange = currentchange
                maxday = alist[0]
            prevpl = pl