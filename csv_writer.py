import csv
import csv_reader as read
from csv import writer
import datetime
from operator import itemgetter
from os import path

sale_sequence = []

def handle_buy(input): 
    current_date = read.read_date()
    product_id = read.get_new_id("bought.csv")
    new_array = [product_id, input['product'], input['quantity'], input['buyprice'], input['exp_date'], current_date]
    if read.check_for_stack(new_array):
        print("We found a duplicate and stacked the items!")
    else:
        with open('bought.csv', 'a', encoding='UTF8', newline='') as buy_list:
            writer = csv.writer(buy_list)
            writer.writerow(new_array) 

def stack_items(quantity, id):
    rows=[]
    with open("bought.csv", newline='') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            rows.append(row)
    for row in rows:
        if row[0] == id:
            row[2] = int(row[2]) + int(quantity)
            with open("bought.csv", 'w', encoding='UTF8', newline='') as buy_list:
                writer = csv.writer(buy_list)
                writer.writerows(rows)

def handle_sell(input):
    name_product = input['product'].lower()
    if read.find_product_name(name_product):
        quantity = read.count_found_product(input['product'].lower())[0]
        row_list = read.count_found_product(input['product'].lower())[1] 
        date_list = read.count_found_product(input['product'].lower())[2]
        if quantity >= input['quantity']:
            total_left = 0
            result = compare_sell_bought(row_list, input['quantity'], quantity) 
            for row in result:
                total_left = int(row[2]) + total_left
            if total_left < input['quantity']:
                print("Damn we dont have enough to forfill your wishes!")
            else: 
                new_date_list = []
                for row in row_list:
                    new_date_list.append(row[4])
                ordered_date_list = (get_date_sequence(new_date_list))
                get_sale_sequence(row_list, ordered_date_list, input['quantity'], input['sellprice'])
        else:
            print("Damn we dont have enough to forfill your wishes!")  
    else:
        print("Product not found!")

def compare_sell_bought(row_list, order_quantity, quantity):
    sold = 0
    new_quantity = quantity
    for row in row_list:
        answer = read.check_sold(row[0], row[2])
        if answer[0] == 'equals':
            row_list.remove(row)
            sold = answer[2]
            new_quantity = new_quantity - sold
            checking(row_list, order_quantity, new_quantity)
            break
        if answer[0] == "less":
            substract = int(row[2]) - int(answer[2])
            row[2] = str(substract)
            sold = answer[2]
            new_quantity = new_quantity - sold
        if answer[0] == 'finished':
            print("")
    return row_list

# Way to order dates i figuered out before I noticed how easy itemgetter is to use for this. I left it here because I kinda liked my workaround. 
def get_date_sequence(date_list):
    date_list.sort(key = lambda date: datetime.datetime.strptime(date, '%Y-%m-%d'))
    return date_list

def get_sale_sequence(row_list, ordered_date_list, q, sp):
    new_list = find_same_value(row_list, ordered_date_list)
    if len(new_list) != 0:
        date_list = []
        for row in new_list:
            date_list.append(row[4])
        ordered_date_list = (get_date_sequence(date_list))
        get_sale_sequence(row_list, ordered_date_list, q, sp)
    else: 
        quantity_countdown(sale_sequence, q, sp)

def quantity_countdown(sale_sequence, quantity_to_sell, sp):
    current_date = read.read_date()
    saleprice = sp
    quantity = quantity_to_sell
    while quantity > 0:
        if int(sale_sequence[0][2]) - quantity < 0:
            quantity = quantity - int(sale_sequence[0][2])
            write_sold(sale_sequence[0][0], sale_sequence[0][2], sp, current_date)
            sale_sequence.remove(sale_sequence[0])
        else:
            write_sold(sale_sequence[0][0], quantity, sp, current_date)
            sale_sequence = []
            break
          
def write_sold(bought_id, quantity, sell_price, current_date):
    selling_id = read.get_new_id("sold.csv")
    new_array = [selling_id, bought_id, quantity, sell_price, current_date]
    with open('sold.csv', 'a', encoding='UTF8', newline='') as sell_list:
        writer = csv.writer(sell_list)
        writer.writerow(new_array)

def find_same_value(row_list, ordered_date_list):
        single_date_list = list(dict.fromkeys(ordered_date_list))
        list_dct = {}
        row_list2 = row_list
        for i in single_date_list:
            list_dct['%s' % i] = []
        for item in row_list:
            if str(item[4]) in list_dct:
                list_dct[str(item[4])] += item
        for key in list_dct:
            if len(list_dct[key]) > 6:
                new_list = []
                for row in row_list2:
                    if row[4] == key:
                        new_list.append(row)
                final_order_list = get_cheap_first(new_list)
                for row in final_order_list:
                    sale_sequence.append(row)
                    row_list2.remove(row)
                break
            else:
                sale_sequence.append((list_dct[key]))
                row_list2.remove((list_dct[key]))
        return row_list2

def get_cheap_first(list):
    return sorted(list, key=itemgetter(3))

def log_date(delta):
    old_date = read.read_date()
    if old_date == "":
        txt = open("current_date.txt", "w")
        txt.write(datetime.datetime.today().strftime('%Y-%m-%d'))
    else:
        old_date_obj = datetime.datetime.strptime(old_date, "%Y-%m-%d")
        new_date = old_date_obj + datetime.timedelta(days=delta)
        txt = open("current_date.txt", "w")
        txt.write(new_date.strftime("%Y-%m-%d"))


def set_new_date(date):
    new_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    txt = open("current_date.txt", "w")
    txt.write(new_date.strftime("%Y-%m-%d"))

def handle_time(input):
    time_change = 0
    if "forwards" in input:
        time_change = (input['forwards'])
    if "backwards" in input:
        time_change = -(input['backwards'])
    if "setdate" in input:
        set_new_date(input['setdate'])
    log_date(time_change)

def write_count_reports():
    with open('reports.csv', newline='') as file:
        reader = csv.reader(file)
        data = list(reader)   
        global rep
        rep = int(data[0][1])
        rep = rep + 1
        data[0][1] = str(rep)
    with open('reports.csv', 'w', encoding='UTF8', newline='') as reports:
        writer = csv.writer(reports)
        writer.writerows(data)

def write_report(input, style, work_date):
    current_date = read.read_date()
    write_count_reports()
    inv_list = ["Product Name", "Quantity", "Buy price", "Exp. date"]
    bal_list = ["Costs", "Income", "Revenue"]
    with open('reports.csv', 'a', encoding='UTF8', newline='') as reports:
        writer = csv.writer(reports)
        writer.writerow(["Report ID:", str(rep)])
        writer.writerow(["------------------------------------------------------------------------------------------------"])
        writer.writerow(["Current date:", current_date])
        writer.writerow(["Report type:", style])
        writer.writerow(["Report date:", work_date])
        if style == "inventory":
            writer.writerow(inv_list)
            for row in input:
                writer.writerow(row)
        if style == "balance":
            writer.writerow(bal_list)
            writer.writerow(input)
        writer.writerow("")
        writer.writerow("")
 

    




    




