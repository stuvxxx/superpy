import datetime
import csv_writer as write
import csv_reader as read
from rich import print
from rich.console import Console
from rich.table import Table
from operator import itemgetter

def yes_or_no(question):
    answer = input(question + "(y/n): ").lower().strip()
    print("")
    while not(answer == "y" or answer == "yes" or \
    answer == "n" or answer == "no"):
        print("Input yes or no")
        answer = input(question + "(y/n):").lower().strip()
        print("")
    if answer[0] == "y":
        return True
    else:
        return False

def handle_report(input):
    if "inventory" in input:
        if 'period' in input:
            print("The period option cannot be used in combination with the inventory option. U may select a period for the balance!")
        else:
            global sort
            if 'sort.p' in input:
                sort = 0
            if 'sort.q' in input:
                sort = 1
            if 'sort.bp' in input:
                sort = 2
            if 'sort.ed' in input:
                sort = 3
            working_date = handle_date(input)
            final_inv = read.calc_inventory(working_date)
            build_inv(final_inv)
    if "balance" in input:
        working_date = handle_date(input)
        final_bal = read.calc_balance(working_date)
        build_bal(final_bal)

def handle_date(input):
    global rep_date
    if "today" in input:
        rep_date = set_inv_date(0)
        return set_inv_date(0)
    if "yesterday" in input: 
        rep_date = set_inv_date(-1)
        return set_inv_date(-1)
    if "period" in input: 
        rep_date = [input['period'][0],input['period'][1]]
        return [input['period'][0],input['period'][1]]
    if "date" in input: 
        rep_date = input['date']
        return input['date']
        
def set_inv_date(delta):
    global rep_date
    current_date = read.read_date()
    working_date = datetime.datetime.strptime(read.read_date(), "%Y-%m-%d")
    new_working_date = working_date + datetime.timedelta(days=delta)
    if delta == 0:
        return current_date
    else:
        return new_working_date.strftime("%Y-%m-%d")

def sort_table(table_list, sort_int):
    sorted_table_list = sorted(table_list, key=itemgetter(sort_int))
    final_sorted_table_list = []
    for row in sorted_table_list:
        new_row = [row[0].lower(), str(row[1]), str(row[2]), row[3]]
        final_sorted_table_list.append(new_row)
    return final_sorted_table_list

def build_inv(input):
    final_table = []
    table_input = []
    table = Table(title="Inventory")
    table.add_column("Product Name", style="cyan")
    table.add_column("Quantity", style="magenta", justify="right")
    table.add_column("Buy price", style="Green", justify="right")
    table.add_column("Exp. date", style="yellow")
    for row in input:
        new_row = [row[1].lower(), int(row[2]), float(row[3]), row[4]]
        table_input.append(new_row)
    if 'sort' in globals():
        table_input = sort_table(table_input, sort)
    else:
        unsorted_table_input = []
        for row in table_input:
            new_row = [row[0].lower(), str(row[1]), str(row[2]), row[3]]
            unsorted_table_input.append(new_row)
            table_input = unsorted_table_input
    for row in table_input:
        table.add_row(row[0], row[1], row[2], row[3])
    console = Console()
    console.print(table)
    if yes_or_no("Do you want to save your report?") == True:
        write.write_report(table_input, "inventory", rep_date)
        print("Report saved! ID number is: ", str(write.rep))
    else: 
        print("All good!")

def build_bal(input):
    table = Table(title="Balance " + str(input[3]))
    table.add_column("Costs", style="red")
    table.add_column("Income", style="blue")
    table.add_column("Revenue", style="Green")
    table_input = [str(input[0]), str(input[1]), str(input[2])]
    table.add_row(table_input[0],table_input[1],table_input[2])
    console = Console()
    console.print(table)
    if yes_or_no("Do you want to save your report?") == True:
        write.write_report(table_input, "balance", rep_date)
        print("Report saved! ID number is: ", str(write.rep))
    else: 
        print("All good!")
