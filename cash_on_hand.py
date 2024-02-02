from pathlib import Path
import csv

def get_deficit_amount(deficit_record):
    """ created to find and return top 3 cash deficits amount """
    return deficit_record[1]  # Assuming the second element is the deficit amount

def processcohdata():
    # create a file path to csv file
    fp = Path.cwd() / "csv_reports" / "Cash_On_Hand.csv"

    # initialize variables
    prevcoh = 0
    maxchange = 0
    maxday = None
    maxloss = 0
    maxlossday = 0
    increases = 0
    decreases = 0
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
            day = alist[0]  # Assuming the first element of alist is the day
            coh = int(alist[1])  # convert into int
            currentchange = coh - prevcoh
            # Tally up the increments
            if coh > prevcoh:
                increases += 1
            # Tally up the decrements
            if coh < prevcoh:
                decreases += 1
                # Append day first, then the absolute value of the deficit
                all_losses.append((day, abs(currentchange)))
                if maxloss < abs(currentchange):
                    maxloss = abs(currentchange)
                    maxlossday = day
            if abs(currentchange) > abs(maxchange):
                maxchange = currentchange
                maxday = day
            prevcoh = coh

    # output file path
    fp = Path.cwd() / "summary_report.txt"
    fp.touch()
    with fp.open(mode="a", encoding="UTF-8") as file:
        # Output based on the analysis
        if decreases == 0:
            file.write("[CASH SURPLUS] CASH ON EACH DAY IS HIGHER THAN THE PREVIOUS DAY\n")
        elif increases == 0:
            file.write("[CASH DEFICIT] CASH ON EACH DAY IS LOWER THAN THE PREVIOUS DAY\n")
        else:
            for day, amount in all_losses:
                file.write(f"\n[CASH DEFICIT] DAY: {day}, AMOUNT: SGD {amount}")

        # Finding the top 3 deficits
        all_losses.sort(key=get_deficit_amount, reverse=True)  # Sort by deficit amount, descending
        top_deficits = all_losses[:3]  # Take the top 3 elements

        # Print the top 3 deficits
        deficit_rank = ["HIGHEST CASH DEFICIT", "2ND HIGHEST CASH DEFICIT", "3RD HIGHEST CASH DEFICIT"]
        for i, (day, amount) in enumerate(top_deficits):
            title = deficit_rank[i] if i < len(deficit_rank) else f"{i+1}TH HIGHEST CASH DEFICIT"
            file.write(f"\n[{title}] DAY: {day}, AMOUNT: SGD {amount}")


