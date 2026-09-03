#!/usr/bin/env python3

import argparse
import csv
import datetime
import os
import re

from dateutil.relativedelta import relativedelta
from tabulate import tabulate

INTEREST_RATE = 0.0699
STARTING_BALANCE = 732000.00
START_DATE = datetime.datetime(2024, 7, 1)
TERM_YRS = 30
TERM_MONTHS = TERM_YRS * 12
PNI_AMOUNT = 4865.10
LAST_PNI_AMOUNT = 4864.29 # not sure how this is calculated

def convert_currency_string_to_float(currency_string):
    """
    Converts a currency string "$###.##" to the
    equivalent floating point value

    :param currency_string: current string in the format "$###,###.##"
    :type currency_string: string
    :return: string
    """
    return float("".join(re.findall("[\d\.]", currency_string)))

class Payment:

    def __init__(self, data_dict):
        """
        Parses payment info from a dict

        Expected dict format:
            "Date": date in MM/DD/YYYY format
            "Principal": interest in $####.## string format
            "Interest": interest in $####.## string format
            "P&I": optional principal & interest in $####.## string format
            "Balance": interest in $####.## string format
        """
        self.idx = int(data_dict["#"])

        date_split = data_dict["Date"].split("/")
        self.date = datetime.datetime(int(date_split[2]), int(date_split[0]), int(date_split[1]))

        self.interest = convert_currency_string_to_float(data_dict["Interest"])
        self.principal = convert_currency_string_to_float(data_dict["Principal"])
        self.ending_balance = convert_currency_string_to_float(data_dict["Balance"])

        if "P&I" in data_dict.keys():
            self.p_and_i = convert_currency_string_to_float(data_dict["P&I"])
        else:
            self.p_and_i = self.interest + self.principal

        self.starting_balance = self.ending_balance + self.principal

    def get_next_payment_date(self):
        day = int(self.date.strftime("%d"))
        month = int(self.date.strftime("%m"))
        year = int(self.date.strftime("%Y"))

        next_payment_day = 1
        next_payment_month = month + 1
        next_payment_year = year

        if next_payment_month > 12:
            next_payment_month = 1
            next_payment_year = year + 1

        next_payment_date = datetime.datetime(
            next_payment_year, next_payment_month, next_payment_day
        )

        return next_payment_date.strftime("%m/%d/%Y")

    def get_formatted_date(self):
        return self.date.strftime("%m/%d/%Y")

    def __str__(self):
        return "Payment #{:03}: {} ".format(
            self.idx,
            self.get_formatted_date()) + ",".join([
                "${:,.2f}".format(self.p_and_i),
                "${:,.2f}".format(self.principal),
                "${:,.2f}".format(self.interest),
                "${:,.2f}".format(self.ending_balance)
            ]
        )

def generate_original_payment_schedule(output_file=None):
    """
    Generates the original payment schedule
    """
    curr_balance = STARTING_BALANCE
    curr_date = START_DATE

    table_data = [[
        "#",
        "Date",
        "P&I",
        "Principal",
        "Interest",
        "Balance",
    ]]

    total_principal = 0
    total_interest = 0

    for i in range(TERM_MONTHS):

        if curr_balance < PNI_AMOUNT:
            curr_pni_amount = LAST_PNI_AMOUNT
        else:
            curr_pni_amount = PNI_AMOUNT

        curr_principal = round(curr_pni_amount - (curr_balance * (INTEREST_RATE / 12)), 2)
        curr_interest = round(curr_pni_amount - curr_principal, 2)

        curr_balance = round(curr_balance - curr_principal, 2)
        #print("{}: {}".format((i + 1), curr_principal))

        table_data.append([
            "{:03}".format((i + 1)),
            curr_date.strftime("%m/%d/%Y"),
            "${:,.2f}".format(curr_pni_amount),
            "${:,.2f}".format(curr_principal),
            "${:,.2f}".format(curr_interest),
            "${:,.2f}".format(curr_balance)
        ])

        total_principal += curr_principal
        total_interest += curr_interest
        curr_date += relativedelta(months=1)

    #print(tabulate(table_data, headers="firstrow") + "\n")
    #print("Total principal: ${:,.2f}".format(total_principal))
    #print("Total interest: ${:,.2f}".format(total_interest))

    if output_file is not None:
        with open(output_file, "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = table_data[0])

            writer.writeheader()
            for i in range(1, len(table_data)):
                row = table_data[i]
                d = {}
                for j in range(len(table_data[0])):
                    d[table_data[0][j]] = row[j]

                writer.writerow(d)

def get_history(history_file):
    """
    Reads history data
    """

    table_data = [[
        "#",
        "Date",
        "P&I",
        "Principal",
        "Interest",
        "Balance",
    ]]

    payment_history = []

    with open(history_file, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            payment_history.append(Payment(row))

    return payment_history

def get_next_payment(last_payment):
    """
    Determines information of the next payment

    :param last_payment: last payment
    :type last_payment: Payment object
    """

    if last_payment.ending_balance < PNI_AMOUNT:
        final_payment_data = {
            "#": last_payment.idx + 1,
            "Date": last_payment.get_next_payment_date(),
            "Principal": "${:,.2f}".format(last_payment.ending_balance),
            "Interest": "${:,.2f}".format(0),
            "Balance": "${:,.2f}".format(0),
        }

        return Payment(final_payment_data)

    next_principal = round(
        PNI_AMOUNT - (
            last_payment.ending_balance * (INTEREST_RATE / 12)
        ),
        2
    )

    next_interest = PNI_AMOUNT - next_principal
    new_balance = last_payment.ending_balance - next_principal

    next_payment_data = {
        "#": last_payment.idx + 1,
        "Date": last_payment.get_next_payment_date(),
        "Principal": "${:,.2f}".format(next_principal),
        "Interest": "${:,.2f}".format(next_interest),
        "Balance": "${:,.2f}".format(new_balance),
    }

    return Payment(next_payment_data)

def get_remaining_payments(payment_history):
    """
    Projects remaining payments until the end of the loan

    :param payment_history: history of payments so far
    :type payment_history: list of Payment objects
    :return: list of remaining Payment objects
    """
    complete_history = list(payment_history)

    while complete_history[-1].ending_balance > 0:# and complete_history[-1].ending_balance >= PNI_AMOUNT:
        next_payment = get_next_payment(complete_history[-1])
        #print(next_payment)
        complete_history.append(next_payment)

    return complete_history

def history_to_table(payment_history):
    """
    Formats history as a table
    """
    table = [["#", "Date", "P&I", "Principal", "Interest", "Balance"]]

    for p in payment_history:
        table.append([
            p.idx,
            p.get_formatted_date(),
            "${:,.2f}".format(p.p_and_i),
            "${:,.2f}".format(p.principal),
            "${:,.2f}".format(p.interest),
            "${:,.2f}".format(p.ending_balance),
        ])

    return tabulate(table, headers="firstrow")

parser = argparse.ArgumentParser()
parser.add_argument("--history", required=True, help="Payment history data in CSV format")
parser.add_argument("--original", required=True, help="Output file for original amortization schedule")
args = parser.parse_args()

# process input
history_file = os.path.abspath(args.history)
if not os.path.exists(history_file):
    print("Could not find {}!".format(history_file))
    exit(1)

original_schedule_file = os.path.abspath(args.original)

generate_original_payment_schedule(original_schedule_file)
payment_history = get_history(history_file)
print(payment_history[-2])
print(payment_history[-1])
print(get_next_payment(payment_history[-1]))
projected_history = get_remaining_payments(payment_history)
print(history_to_table(projected_history))
exit()

with open(history_file, "r") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        print(row["Date"])
