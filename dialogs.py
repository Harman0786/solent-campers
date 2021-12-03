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

class AdvisorDialog:
    def __init__(self, parent):
        self.dialog = tk.Toplevel(parent)
        self.dialog.grab_set()

        regionLabel = tk.Label(self.dialog, text="Select Region")
        regionLabel.pack(side=tk.TOP, pady=(20,0))

        self.region = tk.StringVar()
        self.region.set("North East")

        self.camper = tk.StringVar()
        self.camper.set("Small")

        self.camp = tk.StringVar()
        self.camp.set("")

        self.campList = []
        self.campersType = ["Small", "Medium", "Large"]
        self.regioList = ["North East", "North West", "Yorkshire", "East Midlands", "West Midlands", "South East"]

        labelvan = tk.Label(self.dialog, text="Van Type")
        labelvan.pack(side=tk.TOP, pady=(5,0))

        optionVan = tk.OptionMenu(self.dialog, self.camper, *self.campersType)
        optionVan.pack(side=tk.TOP)

        labelregion = tk.Label(self.dialog, text="Region")
        labelregion.pack(side=tk.TOP, pady=(5,0))

        optionRegion = tk.OptionMenu(self.dialog, self.region, *self.regioList, command=self.omChanged)
        optionRegion.pack(side=tk.TOP)
        
        labelcamp = tk.Label(self.dialog, text="Camp Name")
        labelcamp.pack(side=tk.TOP, pady=(5,0))

        self.optionCamp = tk.OptionMenu(self.dialog, self.camp, self.campList)   

        self.bookButton = tk.Button(self.dialog, text="Book", command=self.saveBooking)

        self.dialog.title('Advisor - Solent Campers')
        self.dialog.geometry("400x350+400+100")

    def omChanged(self, region):

        camps = []
        if not os.path.isfile('campData.csv'):
            messagebox.showerror(master=self.dialog, title="File Not Found", message="Sorry the program could not find the required files")
            return
        else:
            f = open('data/campData.csv', 'r')
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                if int(row[2]) == region:
                    camps.append(row)

            f.close()

            if not len(camps) == 0:
                self.campList = camps
                self.camp.set(camps[0][1])
                menu = self.optionCamp["menu"]
                menu.delete(0, "end")
                for value in self.campList:
                    menu.add_command(label=value[1], command=lambda v=value[1]: self.camp.set(v))

                campLabel = tk.Label(self.dialog, text="Select Region")
                campLabel.pack(side=tk.TOP, pady=(20,0))
                self.optionCamp.pack(side=tk.TOP, pady=(0,30))
                self.bookButton.pack(side=tk.TOP)
            else:
                messagebox.showerror(master=self.dialog, title="Sorry", message="No Camping Site Added in this region. Contact Administrator.")
                return
        

    def saveBooking(self):
        bookingID = random.randint(0, 50)