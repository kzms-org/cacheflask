# imports
import json
import pandas as pd
import numpy as np
import functools
from flask import Flask, request, render_template
import requests


# Appconfig
app = Flask(__name__)

# Routes and their functions

# default route just to test the connection
@app.route('/')
def index():
    return '<p>works</p>'

# CSV preprocessing route that will return a json object with all transactions
@app.route('/csvPreProcessing', methods= ['GET', 'POST'])
def csvPreProcessing():
    print("inside csvpreprocessing")
    if request.method == "POST":
        print(request.files['file'].filename)

        if request.files['file'].filename != None:
            print("has receipt report.csv")
            csv_file = request.files['file']
            df = pd.read_csv(csv_file)
            print(df)
            df_1 = df.iloc[:11,:]
            df_2 = df.iloc[12:,:]

            df_dup = df_1.iloc[2:3,:]

            df_info = df_dup.copy()
            df_info.rename(columns={'Statement Date': 'Currency',
                                            list(df_info)[1]: 'Account_Number',
                                            'Alinma ID number': 'Customer_Name'}, inplace=True)
                                            
            df_info.drop(columns=[list(df_info)[3], 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6'],axis=1, inplace=True)

            """# Transactions Part"""

            df_Transactions = df_2.copy()
            df_Transactions.rename(columns={'Statement Date': 'Date',
                                            list(df_Transactions)[1]: 'Channel',
                                            'Alinma ID number': 'Transaction_Description',
                                            list(df_Transactions)[3]: 'Reference_Number',
                                            'Unnamed: 4': 'Debit',
                                            'Unnamed: 5': 'Credit',
                                            'Unnamed: 6': 'Balance'}, inplace=True)


            df_Transactions = df_Transactions.iloc[1:,:]
            df_Transactions.reset_index(drop=True, inplace=True)

            """# Edit Transaction Table"""

            df_edit = df_Transactions.copy()

            df_edit.reset_index(drop=True, inplace=True)

            df_edit = df_edit.where(pd.notnull(df_edit), None)

            df_edit['Date'] = df_edit['Date'].astype('datetime64')

            df_col = df_edit.copy()
            df_col['Debit'] = df_col['Debit'].str.replace(',','')
            df_col['Credit'] = df_col['Credit'].str.replace(',','')
            df_col['Balance'] = df_col['Balance'].str.replace(',','')

            df_col['Debit'] = df_col['Debit'].astype('float')
            df_col['Credit'] = df_col['Credit'].astype('float')
            df_col['Balance'] = df_col['Balance'].astype('float')

            """# Creating a Item/shop column"""

            df_beta = df_col.copy()

            start_list = ('from', 'FROM', 'Transaction')
            end_list   = ('SAR', 'USD')

            df_beta['no_preceders'] = df_beta.Transaction_Description.apply(
                                    to_apply(remove_preceders, 
                                            start_list)
                                        )
            df_beta['no_succeders'] = df_beta.Transaction_Description.apply(
                                    to_apply(remove_succeeders, 
                                            end_list)
                                        )
            df_beta['Store_or_Item'] = df_beta.no_preceders.apply(
                                    to_apply(remove_succeeders, 
                                            end_list)
                                        )

            df_beta = df_beta.where(pd.notnull(df_beta), None)

            df_beta.drop(columns=['no_preceders', 'no_succeders', 'Transaction_Description'],axis=1, inplace=True)

            # Preparing The needed CSV files

            ## Transaction Dataset"""

            df_Debit  = df_split.iloc[:,3:4]
            df_Credit = df_split.iloc[:,4:5]
            df_Item   = df_split.iloc[:,6:]

            df_Trans = pd.concat([df_Date, df_Debit, df_Credit, df_Item], axis=1)

            df_Spendings = df_Trans.query(' Debit > 0 ')
            df_Spendings.reset_index(drop=True, inplace=True)
            df_Spendings.drop(columns=['Credit'],axis=1, inplace=True)

            df_Spendings['Date'] = df_Spendings['Date'].astype(str)
            spend_dict = df_Spendings.to_dict('records')

            with open("Spend.json", "w") as outfile:
                json.dump(spend_dict, outfile)

            df_Earnings = df_Trans.query(' Credit > 0')
            df_Earnings.reset_index(drop=True, inplace=True)
            df_Earnings.drop(columns=['Debit'],axis=1, inplace=True)

            df_Earnings['Date'] = df_Earnings['Date'].astype(str)
            earn_dict = df_Earnings.to_dict('records')

            with open("Earn.json", "w") as outfile: 
                json.dump(earn_dict, outfile)
    
            return json.dump(earn_dict)

        else: 
            return "file not found"
    else:
        return "Could not handle request"


def remove_preceders(start_list, string):
        for word in start_list:
            if word in string:
                string = string[string.find(word) + len(word):]
        return string

def remove_succeeders(end_list, string):
    for word in end_list:
        if word in string:
            string = string[:string.find(word)]
    return string

def to_apply(func, words_to_check):
    return functools.partial(func, words_to_check)

# get user info (TEST)
@app.route('/api/userinfo')
def userinfo():
    return {'data': "Abdur Rahman"}, 200

# routes to this page if an incorrect url is entered
@app.errorhandler(404)
def page_not_found(e):
    return {'message': "ERROR 404"}, 404

if __name__ == '__main__':
    app.run(debug = True)
