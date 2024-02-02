# importing cash on hand, profit and loss, and overheads.
import cash_on_hand
import overheads
import profit_loss

def main():
    # sort the datas, writing results into the summary report
    overheads.sort_overheads()
    cash_on_hand.processcohdata()
    profit_loss.processpaldata()
main()