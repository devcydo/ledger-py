from ast import Continue
import colorsys
from contextvars import copy_context
import os.path
import argparse
import re
from datetime import datetime

#Required classes
import classes.transaction as transaction
import classes.concept as concept
from classes.colors import bcolors

def balance(filename):
    if not os.path.isfile(fileName):
        print('File does not exist.')
    else:
        #read file content
        with open(fileName,'r') as f:
            content = f.read().splitlines()
        
        #Process content
        transactions = getTransactions(content)

        for _t in transactions:
            ...


def printFile(fileName, sort_param):
    if not os.path.isfile(fileName):
        print('File does not exist.')
    else:
        #read file content
        with open(fileName,'r') as f:
            content = f.read().splitlines()
        
        #Process content
        transactions = getTransactions(content)

        if sort_param != None:
            transactions = sortTransactions(sort_param, transactions)
        #print
        for _t in transactions:
            print("{:<20} {:<10}".format(
                colorString('gray',_t.date), 
                _t.description
            ))
            for c in _t.concepts:
                #Check color for amount
                if float(c.amount) < 0:
                    color = 'red'
                else:
                    color = 'green'
                if c.currency == '$':                
                    print("{:<10} {:<10}".format(
                        colorString('blue', c.description), 
                        colorString(color, c.currency + c.amount)
                    ))
                else:
                    print("{:<10} {:<10}".format(
                        colorString('blue', c.description), 
                        colorString(color, c.amount + ' ' + c.currency)
                    ))

def register(fileName, sort_param):
    if not os.path.isfile(fileName):
        print('File does not exist.')
    else:
        #read file content
        with open(fileName,'r') as f:
            content = f.read().splitlines()
        
        #Process content
        transactions = getTransactions(content)

        if sort_param != None:
            transactions = sortTransactions(sort_param, transactions)
        #print
        for _t in transactions:
            #Check color for amount
            if float(_t.concepts[0].amount) < 0:
                color = 'red'
            else:
                color = 'green'
            if _t.concepts[0].currency == '$':
                print()
                print("{:<10} {:<30} {:<10} {:<20} {:<20}".format(
                    colorString('gray',_t.date), 
                    _t.description, 
                    colorString('blue',_t.concepts[0].description), 
                    colorString(color,_t.concepts[0].currency + _t.concepts[0].amount), 
                    colorString(color,_t.concepts[0].currency + _t.concepts[0].amount)
                ))
            else:
                print("{:<10} {:<30} {:<10} {:<20} {:<20}".format(
                    colorString('gray',_t.date), 
                    _t.description, 
                    colorString('blue',_t.concepts[0].description), 
                    colorString(color,_t.concepts[0].amount + ' ' + _t.concepts[0].currency), 
                    colorString(color,_t.concepts[0].amount + ' ' + _t.concepts[0].currency)
                ))
            for c in _t.concepts[1:]:
                if c.currency == '$':
                    print("{:<10} {:<30} {:<10} {:<20} {:<20}".format(
                        '',
                        '',
                        colorString('blue', c.description), 
                        colorString(color, c.currency + c.amount), 
                        colorString(color, c.currency + c.amount)
                    ))
                else:
                    print("{:<10} {:<30} {:<10} {:<20} {:<20}".format(
                        '',
                        '',
                        colorString('blue', c.description), 
                        colorString(color, c.amount + c.currency), 
                        colorString(color, c.amount + c.currency)
                    ))

def sortTransactions(by, transactions):
    if by == 'date' or by == 'd':
        return sorted(transactions, key=lambda x: x.date, reverse=False)
    else: 
        return transactions

#=== GENERAL FUNCTIONS ===#

def getTransactions(content):
    t = transaction.Transaction()
    transactions = []
    concepts = []

    for line in content:
        c = concept.Concept()
        if line[0].isdigit():
            #Create and append transaction
            if len(concepts) > 0:
                t.concepts = concepts
                transactions.append(t)
                t = transaction.Transaction()
                concepts = []
            t.date = formatDate(line)
            t.description = line.split(' ',1)[1]
        #Create concepts array
        elif line[0] != ';':
            a = re.split(r"([-|$|\d])", line, 1, flags=re.I)
            #check if there is a value in the array
            if len(a) > 1:
                c.description = a[0]
                c.amount, c.currency = convertAmount(a[1:])
            else:
                c.description = a[0]
            concepts.append(c)
    else:
        t.concepts = concepts
        transactions.append(t)
    
    return transactions

def formatDate(line):
    #Search for date
    date = re.search(r'\d{4}/\d{1,2}/\d{1,2}', line)
    #Create datetime object
    date = datetime.strptime(date.group(), '%Y/%m/%d').date()
    #Change format of datetime object
    date = date.strftime('%y-%b-%d')
    return date

def colorString(color, string):
    switch = {
        'gray': bcolors.GRAY,
        'red': bcolors.RED,
        'green': bcolors.GREEN,
        'yellow': bcolors.YELLOW,
        'blue': bcolors.BLUE,
    }
    return switch.get(color,'') + string + bcolors.ENDC

def convertAmount(array):
    if array[0] == '$':
        currency = array[0]
        amount = array[1]
    else:
        if array[1][0] != ' ':
            currency = array[1].split()[1]
            amount = array[0] + array[1].split()[0]
        else:
            currency = array[1].split()[0]
            amount = array[0]

    return amount, currency
#=== GENERAL FUNCTIONS ===#

def main():
    # create parser
    parser = argparse.ArgumentParser(
        prog='LedgerPy',
        description='Simple implementation of Ledger CLI',
        epilog='Ledger implementation by Luis Martinez'
    )
    
    # add arguments to the parser
    parser.add_argument("command")
    parser.add_argument("fileName")
    parser.add_argument('--sort', nargs='?', const=1, type=str)
    parser.add_argument('--file', nargs='?', const=1, type=str)
    parser.add_argument('--price-db', nargs='?', const=1, type=str)
    
    # parse the arguments
    args = parser.parse_args()

    # get the arguments value
    if args.command == 'reg' or args.command == 'register':
        register(args.fileName, args.sort)
    elif args.command == 'bal' or args.command == 'balance':
        balance(args.fileName)
    elif args.command == 'pr' or args.command == 'print':
        printFile(args.fileName, args.sort)
    else:
        print("Please, enter a valid command.")
        print("For more help run the program with the option: -h")

if __name__ == "__main__":
    main()