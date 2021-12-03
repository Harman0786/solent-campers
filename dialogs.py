import tkinter as tk
from  tkinter import ttk
from tkinter import messagebox
import random, os, datetime, csv, json

class CustomerDialog:
    def __init__(self, parent):
        self.dialog = tk.Toplevel(parent)

        bookingTable = ttk.Treeview(self.dialog)
        bookingTable['columns'] = ('id', 'camp', 'van', 'region', 'date')

        bookingTable.column("#0", width=0,  stretch=tk.NO)
        bookingTable.column("id", anchor=tk.CENTER, width=80)
        bookingTable.column("camp",anchor=tk.CENTER, width=80)
        bookingTable.column("van",anchor=tk.CENTER, width=80)
        bookingTable.column("region",anchor=tk.CENTER, width=80)
        bookingTable.column("date",anchor=tk.CENTER, width=80)

        bookingTable.heading("#0",text="",anchor=tk.CENTER)
        bookingTable.heading("id",text="Id",anchor=tk.CENTER)
        bookingTable.heading("camp",text="Camp",anchor=tk.CENTER)
        bookingTable.heading("van",text="Van",anchor=tk.CENTER)
        bookingTable.heading("region",text="Region",anchor=tk.CENTER)
        bookingTable.heading("date",text="Date",anchor=tk.CENTER)

        rows = []
        if os.path.isfile('data/bookings.csv'):
            f = open('data/bookings.csv', 'r', newline='', encoding='utf-8')
            reader = csv.reader(f)
            header = next(reader)
            id = 0
            for row in reader:
                bookingTable.insert(parent='',index='end',iid=id, text='',values=(row[0], row[1], row[2], row[3], row[4]))
                id = id+1
            f.close()

            bookingTable.pack(side=tk.TOP)
            buttonExport = tk.Button(self.dialog, text="Export Data", height=3, width=15, command=self.exportData)
            buttonExport.pack(side=tk.TOP)

            for row in rows:
                row.pack(side=tk.TOP)
        else:
            errorLable = tk.Label(self.dialog, text="Sorry, You got no bookings!")
            errorLable.pack(side=tk.TOP, pady=(50,0))      

        self.dialog.title('Customer - Solent Campers')
        self.dialog.geometry("400x500+400+100")
        

    def exportData(self):
        if os.path.isfile('data/bookings.csv'):
            f = open('data/bookings.csv', 'r', newline='', encoding='utf-8')
            reader = csv.reader(f)
            header = next(reader)
            bookingList = []
            for row in reader:
                booking = {
                    "booking_id": row[0],
                    "camp_name": row[1],
                    "camper_type": row[2],
                    "region_name": row[3],
                    "booking_date": row[4]
                }

                bookingList.append(booking)

            with open("export.json", "a") as outF:
                outF.write(json.dumps(bookingList, indent = 4))
            f.close()