# pulling data from csv files
from pathlib import Path
import csv

def sort_overheads():
    # create a file path to csv file
    fp = Path.cwd() / "csv_reports" / "Overheads.csv"

    # read the csv file
    with fp.open(mode="r", encoding="UTF-8", newline="") as file:
        lists = csv.reader(file)
        next(lists)  # skip header

        overheads_list = []

        # convert data to a usable format and skip the header
        for item in lists:
            first_element = item[0]
            second_element_as_float = float(item[1])
            modified_item = [first_element, second_element_as_float]
            overheads_list.append(modified_item)

    # implementing a simple sort scenerio to sort the overheads_list
    n = len(overheads_list)
    for i in range(n):
        for j in range(0, n-i-1):
            # taking only the highest percentage overheads
            if overheads_list[j][1] < overheads_list[j+1][1]:
                overheads_list[j], overheads_list[j+1] = overheads_list[j+1], overheads_list[j]

    
    # output file path
    fp = Path.cwd() / "summary_report.txt"
    fp.touch()
    with fp.open(mode="a", encoding="UTF-8") as file:
        # write the highest overhead to the file
        if overheads_list:
            highest_overhead = overheads_list[0]
            file.write( f"[HIGHEST OVERHEAD] {highest_overhead[0]}: {highest_overhead[1]}%")