import csv
import csv_writer
from datetime import datetime


def read_date():
    f = open("current_date.txt", "r")
    return f.read()

def get_new_id(file):
  row_count = 0
  with open(file, 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader: 
      row_count = row_count +1
  return row_count

def check_for_stack(input):
  with open("bought.csv", 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
      if row[1].lower() == input[1].lower() and row[3] == str(input[3]) and row[4] == input[4] and row[5] == input[5]:
        csv_writer.stack_items(input[2], row[0])
        return True

def find_product_name(name_product):
  with open("bought.csv", 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
      if row[1].lower() == name_product:
        return True

def count_found_product(name):
  quantity = 0
  row_list = []
  date_list = []
  current_date_string = read_date()
  current_date = datetime.strptime(current_date_string, "%Y-%m-%d")
  with open("bought.csv", 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
      if row[1].lower() == name and datetime.strptime(row[5], "%Y-%m-%d") <= current_date:
        row_list.append(row)
        quantity = int(row[2]) + quantity
        date_list.append(row[4])
  return [quantity, row_list, date_list]     

def count_stuff(id):
  with open("sold.csv", 'r') as file:
    csvreader = csv.reader(file)
    total_amount = 0
    for row in csvreader:
      if row[1] == id:
        total_amount = total_amount + int(row[2])
  return total_amount
        
def check_sold(id, quantity):
  id_to_remove_list = []
  total_amount = count_stuff(id)
  if total_amount != 0:   
    with open("sold.csv", 'r') as file:
      csvreader = csv.reader(file)
      for row in csvreader:
        if total_amount == 0:
            break
        if row[1].isnumeric():
          if row[1] == id and int(quantity) == total_amount:
            return ['equals', id, total_amount]
            break
          if row[1] == id and int(quantity) > total_amount:
            return ['less', id, total_amount]
  return ['finished']

def check_sold_inventory(id):
  with open("sold.csv", 'r') as file:
      csvreader = csv.reader(file)
      quantity_sold = 0
      for row in csvreader:
        if row[1] == id:
          quantity_sold = int(row[2]) + quantity_sold
  return quantity_sold

def calc_inventory(date):
  row_list = []
  with open("bought.csv", 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
      if row[0].isnumeric():
        if datetime.strptime(row[5], "%Y-%m-%d") <= datetime.strptime(date, "%Y-%m-%d"):
          quantity_sold = check_sold_inventory(row[0])
          if quantity_sold == 0:
            row_list.append(row)
          elif quantity_sold < int(row[2]):
            new_quantity_value = int(row[2]) - quantity_sold
            row[2] = str(new_quantity_value)
            row_list.append(row)
  return row_list

def calc_balance(date):
  total_costs = 0
  total_income = 0
  if type(date) is list:
    with open("bought.csv", 'r') as file:
      csvreader = csv.reader(file)
      for row in csvreader:
        if row[0].isnumeric():
          if datetime.strptime(row[5], "%Y-%m-%d") >= datetime.strptime(date[0], "%Y-%m-%d") and datetime.strptime(row[5], "%Y-%m-%d") <= datetime.strptime(date[1], "%Y-%m-%d"):
            total_costs = total_costs + int(row[2]) * float(row[3])
    with open("sold.csv", 'r') as file:
      csvreader = csv.reader(file)
      for row in csvreader:
        if row[0].isnumeric():
          if datetime.strptime(row[4], "%Y-%m-%d") >= datetime.strptime(date[0], "%Y-%m-%d") and datetime.strptime(row[4], "%Y-%m-%d") <= datetime.strptime(date[1], "%Y-%m-%d"):
            total_income = total_income + int(row[2]) * float(row[3])
  else:
    with open("bought.csv", 'r') as file:
      csvreader = csv.reader(file)
      for row in csvreader:
        if row[0].isnumeric():
          if datetime.strptime(row[5], "%Y-%m-%d") == datetime.strptime(date, "%Y-%m-%d"):
            total_costs = total_costs + int(row[2]) * float(row[3])
    with open("sold.csv", 'r') as file:
      csvreader = csv.reader(file)
      for row in csvreader:
        if row[0].isnumeric():
          if datetime.strptime(row[4], "%Y-%m-%d") == datetime.strptime(date, "%Y-%m-%d"):
            total_income = total_income + int(row[2]) * float(row[3])
  total_revenue = total_income - total_costs
  return[total_costs, total_income, total_revenue, date]
