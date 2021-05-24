# Python script QBlix Data Analyst Code - May 2021
# This script transforms a txt in a json format

import json
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from datetime import datetime as dt

Tk().withdraw()
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

qplix_dict = {'QplixTransformation': []}  # Create Json output dictionary
current_positions = {'CurrentPositions': []}  # Create Positions dictionary
current_balances = {'CurrentBalances': []}  # Create Balance dictionary
transactions = {'Transactions': []}  # Create Transactions dictionary
result = {'AffectedPosition': []}  # Create a dictionary for Affected Positions by transactions

# open input file
with open(filename) as fh:
    for line in fh:
        # Create temp-dictionaries for Json Output
        # CustodianAccount informations in dictionary
        customer_account = {'CustodianAccountReference': {'ReferenceType': 'ByExternalID', 'Number': int},
                            'PositionReference': {'ReferenceType': 'ISIN', 'ISIN': str}, 'Quantity': int}
        # Balances informations in dictionary
        custodian_account = {'CustodianAccount': {'ReferenceType': 'ByExternalID', 'Number': int},
                             'AccountReference': {'ReferenceType': 'ByExternalId', 'Number': str},
                             'AccountCurrency': str, 'Balance': float, 'AsOf': int}
        # Stocks informations in dictionary
        stocks = {'TransactionId': int, 'TransactionType': str, 'CustomerInformation': customer_account,
                  'AccountReferenceNumber': str, 'TradingCurrency': str, 'TradeQuantity': int, 'TotalAmount': float,
                  'Type': str, 'NumberOfPartialExecution': int, 'Stockprice': float, 'Volume': float,
                  'StockExchange': str, 'OrderFees': float}
        # Transfer informations in dictionary
        transfer = {'TransactionId': int, 'TransactionType': 'CashTransfer', 'CustodianAccountNumber': int,
                    'Currency': str, 'AccountReferenceNumber': str, 'DateOrderCreation': int, 'DateOrderExecution': int,
                    'Amount': int, 'Usage': str, 'Acronym': str}
        # Forex informations in dictionary
        forex_trade = {'TransactionId': int, 'TransactionType': 'ForexTrade', 'CustodianAccountNumber': int,
                       'BaseCurrency': str, 'QuoteCurrency': str, 'DateOrderCreation': int, 'DateOrderExecution': int,
                       'AmountBase': int, 'AmountQuote': int, 'ExchangeRate': float, 'AccountReferenceNumberBase': str,
                       'AccountReferenceNumberQuote': str}

        i = 0 # Iterator
    # reading line by line from the text file
        description = list(line.strip().split(','))
        if description[0]=='Position_Recon':  # Store Positions information to dictionary
            customer_account['CustodianAccountReference']['Number'] = description[1]
            customer_account['PositionReference']['ISIN'] = description[2]
            customer_account['Quantity'] = description[3]
            current_positions['CurrentPositions'].append(customer_account)
        elif description[0] == 'Cash_Recon':  # Store Cash Recon information to dictionary
            custodian_account['CustodianAccount']['Number'] = description[1].strip('USD EUR')
            custodian_account['AccountReference']['Number'] = description[1]
            custodian_account['AccountCurrency'] = description[1].strip('0123456789')
            custodian_account['Balance'] = description[2]
            custodian_account['AsOf'] = description[3]
            date = dt.strptime(description[3], '%Y%m%d')  # transform to date format
            custodian_account['AsOf'] = (date.strftime('%Y-%m-%d'))  # output to date format
            current_balances['CurrentBalances'].append(custodian_account)
        elif description[0] == 'Buy': # Create Buying Stock values
            stocks['TransactionId'] = description[3]
            stocks['TransactionType'] = 'BuyingStocks'
            stocks['CustomerInformation']['CustodianAccountReference']['Number'] = description[4]
            stocks['CustomerInformation']['PositionReference']['ISIN'] = description[6]
            stocks['CustomerInformation']['Quantity'] = 0
            stocks['AccountReferenceNumber'] = description[5]
            while i < (len(current_positions['CurrentPositions'])):  #Get actual position quantity
                if current_positions['CurrentPositions'][i]['CustodianAccountReference']['Number'] == description[4]:
                    if current_positions['CurrentPositions'][i]['PositionReference']['ISIN'] == description[6]:
                        stocks['CustomerInformation']['Quantity'] = current_positions['CurrentPositions'][i]['Quantity']
                    i = i+1
            stocks['TradingCurrency'] = description[7]
            stocks['TradeQuantity'] = "Buy "+description[12]
            stocks['TotalAmount'] = description[20]
            stocks['NumberOfPartialExecution'] = description[9]
            stocks['Stockprice'] = description[11]
            stocks['Volume'] = description[13]
            stocks['Type'] = description[10]
            stocks['StockExchange'] = description[23]
            stocks['OrderFees'] = description[21]
            transactions['Transactions'].append(stocks)
        elif description[0] == 'Sell': # Create Selling Stock values
            stocks['TransactionId'] = description[3]
            stocks['TransactionType'] = 'SellingStocks'
            stocks['CustomerInformation']['CustodianAccountReference']['Number'] = description[4]
            stocks['CustomerInformation']['PositionReference']['ISIN'] = description[6]
            stocks['CustomerInformation']['Quantity'] = 0
            stocks['AccountReferenceNumber'] = description[5]
            while i < (len(current_positions['CurrentPositions'])):  # Get actual position quantity
                if current_positions['CurrentPositions'][i]['CustodianAccountReference']['Number'] == description[4]:
                    if current_positions['CurrentPositions'][i]['PositionReference']['ISIN'] == description[6]:
                        stocks['CustomerInformation']['Quantity'] = current_positions['CurrentPositions'][i]['Quantity']
                    i = i+1
            stocks['TradingCurrency'] = description[7]
            stocks['TradeQuantity'] = "Sell " + description[12]
            stocks['TotalAmount'] = description[23]
            stocks['NumberOfPartialExecution'] = description[9]
            stocks['Stockprice'] = description[11]
            stocks['Volume'] = description[13]
            stocks['Type'] = description[10]
            stocks['StockExchange'] = description[26]
            stocks['OrderFees'] = description[24]
            transactions['Transactions'].append(stocks)
        elif description[0] == 'Cash_Transfer':  # Store Cash Transfer information to dictionary
            transfer['TransactionId'] = description[3]
            transfer['CustodianAccountNumber'] = description[4]
            transfer['Currency'] = description[5].strip('0123456789')
            transfer['AccountReferenceNumber'] = description[5]
            date = dt.strptime(description[1], '%Y%m%d')  # transform to date format
            transfer['DateOrderCreation'] = (date.strftime('%Y-%m-%d'))
            date = dt.strptime(description[2], '%Y%m%d')  # output to date format
            transfer['DateOrderExecution'] = (date.strftime('%Y-%m-%d'))
            transfer['Amount'] = description[6]
            transfer['Usage'] = description[7]
            transfer['Acronym'] = description[8]
            transactions['Transactions'].append(transfer)
        elif description[0] == 'FX_Cash':  # Store Forex Trade information to dictionary
            forex_trade['TransactionId'] = description[3]
            forex_trade['CustodianAccountNumber'] = description[4].strip('0123456789')
            forex_trade['BaseCurrency'] = description[6]
            forex_trade['QuoteCurrency'] = description[8]
            date = dt.strptime(description[1], '%Y%m%d')
            forex_trade['DateOrderCreation'] = (date.strftime('%Y-%m-%d'))  # transform to date format
            ate = dt.strptime(description[2], '%Y%m%d')
            forex_trade['DateOrderExecution'] = (date.strftime('%Y-%m-%d')) # output to date format
            forex_trade['AmountBase'] = description[5]
            forex_trade['AmountQuote'] = description[7]
            forex_trade['ExchangeRate'] = description[9]
            forex_trade['AccountReferenceNumberBase'] = description[4]
            forex_trade['AccountReferenceNumberQuote'] = description[11]
            transactions['Transactions'].append(forex_trade)
        else:
            break

# Get the positions and balances affected by transactions
for elem in (transactions['Transactions']):  # Iterate over transactions
    if (elem['TransactionType'] == 'SellingStocks') | (elem['TransactionType'] == 'BuyingStocks'):
        for elem2 in (current_balances['CurrentBalances']):  # Iterate over balances
            if elem['AccountReferenceNumber'] == elem2['AccountReference']['Number']:  # Get affected balances
                affected_bal = {'AffectedBalances': elem2['AccountReference']}
                #result['AffectedPosition'].append(affected_bal)  # Append to dictionary
        for elem3 in (current_positions['CurrentPositions']):  # Get affected positions
            if elem['CustomerInformation'] ['PositionReference']['ISIN'] == elem3['PositionReference']['ISIN']:
                affected_pos = {'TransactionId': elem['TransactionId'], 'AffectedPositions': elem3['PositionReference'],
                                'AffectedBalances': affected_bal.get('AffectedBalances')}
                result['AffectedPosition'].append(affected_pos)  # Append to dictionary
    if elem['TransactionType'] == 'CashTransfer':  # Get affected Cash transfers
        for elem2 in (current_balances['CurrentBalances']):
            if elem['AccountReferenceNumber'] == elem2['AccountReference']['Number']:
                affected_bal = {'TransactionId': elem['TransactionId'], 'AffectedBalances': elem2['AccountReference']}
                result['AffectedPosition'].append(affected_bal) # Append to dictionary
    if elem['TransactionType'] == 'ForexTrade':  # Get affected Forex trades
        for elem2 in (current_balances['CurrentBalances']):
            if elem['AccountReferenceNumberBase'] == elem2['AccountReference']['Number']:
                affected_bal = {'TransactionId': elem['TransactionId'], 'AffectedBalances': elem2['AccountReference']}
                result['AffectedPosition'].append(affected_bal) # Append to dictionary
                if elem['AccountReferenceNumberQuote'] == elem2['AccountReference']['Number']:
                    affected_bal = {'TransactionId': elem['TransactionId'], 'AffectedBalances': elem2['AccountReference']}
                    result['AffectedPosition'].append(affected_bal)  # Append to dictionary

# Append positions, balances, transactions and affected Balances/Positions of the transactions to Qplix dictionary
qplix_dict['QplixTransformation'].append(result)
qplix_dict['QplixTransformation'].append(current_positions)
qplix_dict['QplixTransformation'].append(current_balances)
qplix_dict['QplixTransformation'].append(transactions)
qplix_dict['QplixTransformation'].append(result)


# Create the Json Output File
out_file = open("target_output_qplix.json", "w")
json.dump(qplix_dict, out_file, indent=4, sort_keys=False)  # Dump Qplix dictionary to Json File
out_file.close()

"""
Next Steps: Create steps in the script as Extract, Load and Transform methods
"""