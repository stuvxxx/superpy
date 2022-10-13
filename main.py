# Imports
import argparse
import csv
import datetime
import os.path 
from os import path
import csv_writer as write
import csv_reader as read
import sys
from rich import print
from rich.console import Console
import report_logic as rl

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
console = Console()
def main():
    parser = argparse.ArgumentParser(prog='Superpy',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=('''\
------------------
WELCOME TO SUPERPY 
------------------

---------------------------------------------------------------------
If this is the first time you open superpy the workingdate is set to 
today. If you used the program before the workingdate is the same as
it was the last time Superpy closed!
---------------------------------------------------------------------

------
ENJOY!
------
                                '''))
    write.log_date(0)
    parser.add_argument('action', choices=['buy', 'sell', 'report', 'time'])
    BuySell = parser.add_argument_group('Buy or sell','To "buy" an item "buy" option and add all the options below with [BUY] in its description. To "sell" an item use the options below with [SELL] in its description.')
    BuySell.add_argument('--product', '-p', default=argparse.SUPPRESS, metavar=(''), help='[buy][sell]: Name of product')
    BuySell.add_argument('--quantity', '-q', default=argparse.SUPPRESS, type=int, metavar=(''), help='[buy][sell]: How many of the product (only digits)')
    BuySell.add_argument('--buyprice', '-bp', default=argparse.SUPPRESS, type=float, metavar=(''), help='[buy]: Buyprice per product.')
    BuySell.add_argument('--sellprice', '-sp', default=argparse.SUPPRESS, type=float, metavar=(''), help='[sell]: Sellprice per product.')
    BuySell.add_argument('--exp-date', '-ed', default=argparse.SUPPRESS, type=str, metavar=(''), help="[buy]: Expiration date in this format: YYYY-MM-DD")
    Report = parser.add_argument_group('Get a report', 'to get a report start with "report" followed by either "--inventory"(to see inventory) or "--balance"(to get a financial overview) you can either select today or yesterday, a specific date or a period, please note that "period" can only be used in combination with --balance. To sort the inventory add one of the sorting options. After your report is shown you will get the option to save your report.')
    Report2 = Report.add_mutually_exclusive_group()
    Report2.add_argument('--inventory', '-i', default=argparse.SUPPRESS, action="store_true", help='Show inventory')
    Report2.add_argument('--balance', '-b', default=argparse.SUPPRESS, action="store_true", help='Show balance')
    Report3 = Report.add_mutually_exclusive_group()
    Report3.add_argument('--today', action="store_true", default=argparse.SUPPRESS, help='Show today')
    Report3.add_argument('--yesterday', action="store_true", default=argparse.SUPPRESS, help='Show yesterday')
    Report3.add_argument('--date', type=str, metavar=(''), default=argparse.SUPPRESS, help='Enter a date')
    Report3.add_argument('--period', metavar=(''), default=argparse.SUPPRESS, help='Enter a period', nargs=2)
    Report4 = Report.add_mutually_exclusive_group()
    Report4.add_argument('--sort.p', action="store_true", default=argparse.SUPPRESS, help='Sort report on product name (a-z)')
    Report4.add_argument('--sort.q', action="store_true", default=argparse.SUPPRESS, help='Sort report on quantity (low-high)')
    Report4.add_argument('--sort.bp', action="store_true", default=argparse.SUPPRESS, help='Sort report on buyprice (low-high)')
    Report4.add_argument('--sort.ed', action="store_true", default=argparse.SUPPRESS, help='Sort report on exp-date (first-last')
    Time = parser.add_argument_group('Change dates', 'With the time option you can change the working date. You can either set a new date or go a number of days either back or forth.')
    Time2 = Time.add_mutually_exclusive_group()
    Time2.add_argument('--setdate', default=argparse.SUPPRESS, type=str, metavar=(''), help='Set a date')
    Time2.add_argument('--forwards', default=argparse.SUPPRESS, type=int, metavar=(''), help='Enter number of days')
    Time2.add_argument('--backwards', default=argparse.SUPPRESS, type=int, metavar=(''), help='Enter number of days')


#argparse menu logic: 

    args = parser.parse_args()
    buy_list = ['action', 'product', 'quantity', 'buyprice', 'exp_date']
    sell_list = ['action', 'product', 'quantity', 'sellprice']
    balance_list = ['action', 'inventory', 'balance', 'today', 'yesterday', 'date', 'period', 'sort.p','sort.q','sort.bp','sort.ed']
    time_list = ['action', 'forwards', 'backwards', 'setdate']
    input_list = []
    missing_list = []
    wrong_list = []

    def check_date(date):
        format = '%Y-%m-%d'
        try:
          datetime.datetime.strptime(date, format)
          return "yes"
        except ValueError:
          console.print('[blue]{0}[/] is the incorrect date string format. It should be YYYY-MM-DD'.format(date))

    if args.action == "buy":
        input = vars(args)
        for key in input.keys(): 
            input_list.append(key)
            if key not in buy_list: 
                wrong_list.append(key)
        for key in buy_list: 
            if key not in input_list:
                missing_list.append(key)
        if missing_list != []:
            console.print("[red]ERROR:[/] You forgot the following arguments: ", missing_list)
        if wrong_list != []:
            console.print("[red]ERROR:[/] Please remove the following arguments: ", wrong_list)
        if input['quantity'] <= 0:
            console.print("[red]ERROR:[/] You cannot add [green]0[/] or a negative amount of stuff here!, please adjust your [green]quanity[/] amount.")
        if input['buyprice'] < 0:
            console.print("[red]ERROR:[/] You cannot add a negative price here!, please adjust your [green]buyprice[/].")
        if check_date(input['exp_date']) == "yes":
            write.handle_buy(input)

    if args.action == "sell":
        input = vars(args)
        for key in input.keys(): 
            input_list.append(key)
            if key not in sell_list: 
                wrong_list.append(key)
        for key in sell_list: 
            if key not in input_list:
                missing_list.append(key)
        if missing_list != []:
            console.print("[red]ERROR:[/] You forgot the following arguments: ", missing_list)
        if wrong_list != [] and wrong_list != ['hico']:
            console.print("[red]ERROR:[/] Please remove the following arguments: ", wrong_list)
        if input['quantity'] <= 0:
            console.print("[red]ERROR:[/] You cannot add [green]0[/] or a negative amount of stuff here!, pls change your [green]quanity[/] amount.")
        if input['sellprice'] < 0:
            console.print("[red]ERROR:[/] You cannot add a negative price here!,  pls change your [green]sellprice[/].")
        else:
            write.handle_sell(input)

    if args.action == "report":
            input = vars(args)
            for key in input.keys(): 
                input_list.append(key)
                if key not in balance_list: 
                    wrong_list.append(key)
            if wrong_list != []:
                console.print("[red]ERROR:[/] Please remove the following arguments: ", wrong_list)
            if "today" in input_list or "yesterday" in input_list or "date" in input_list or "period" in input_list:
                if "date" in input_list:
                    if check_date(input['date']) == "yes":
                        rl.handle_report(input)
                if "period" in input_list: 
                    check_date(input['period'][0])
                    check_date(input['period'][1])
                    rl.handle_report(input)
                if "today" in input_list or "yesterday" in input_list:
                    rl.handle_report(input)   
            else: 
                console.print("[red]ERROR:[/] You forgot one argument, pls use one of the following arguments when asking for a report: [green]--today --yesterday --date --period[/]") 


    if args.action == "time":
        input = vars(args)
        for key in input.keys(): 
            input_list.append(key)
            if key not in time_list: 
                wrong_list.append(key)
        if wrong_list != []:
            console.print("[red]ERROR:[/] Please remove the following arguments: ", wrong_list)
        if "forwards" in input_list or "backwards" in input_list or "setdate" in input_list:
            if "setdate" in input_list:
                check_date(input['setdate'])
        else: 
            console.print("[red]ERROR:[/] Sorry, you forgot one argument, pls use one of the following arguments when you are about to change time: [green]--forwards --backwards or --setdate[/]") 
        write.handle_time(input)

if __name__ == "__main__":
    main()
