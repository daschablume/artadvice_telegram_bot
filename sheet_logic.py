#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 20:44:19 2020

@author: macuser
"""
from random import shuffle
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('googlesheetcreds.json', scope)
client = gspread.authorize(creds)

advice_sheet = client.open('VONOADVICE').worksheet('Advices')
list_of_text = advice_sheet.col_values('1')

archive_advice_sheet = client.open('VONOADVICE').worksheet('Archive')
archive_advice_list =  archive_advice_sheet.col_values('1')

users_advices_sheet = client.open('VONOADVICE').worksheet('Suggestions')


def get_advice_string(lst):
    shuffle(lst)
    if len(lst) > 0:
        a = lst.pop()
        return a 
    return None


def add_advice(txt):
    cell = 'A' + str(len(users_advices_sheet.col_values('1'))+1)
    users_advices_sheet.update(cell, txt)
            
    
if __name__ == '__main__':
    pass