import tkinter as tk
from  tkinter import ttk
from tkinter import messagebox
import random, os, datetime, csv, json

class CustomerDialog:
    def __init__(self, parent):
        self.dialog = tk.Toplevel(parent)

        buttonExport = tk.Button(self.dialog, text="Export Booking Data", height=1, width=20, bg="green", command=self.exportData)
        buttonExport.pack(side=tk.TOP, pady=(20,10))

        bookingTable = ttk.Treeview(self.dialog)
        bookingTable['columns'] = ('id', 'camp_name', 'region_name', 'camper_size', 'date_of_booking')

        bookingTable.column("#0", width=0,  stretch=tk.NO)
        bookingTable.column("id", anchor=tk.CENTER, width=80)
        bookingTable.column("camp_name",anchor=tk.CENTER, width=80)
        bookingTable.column("region_name",anchor=tk.CENTER, width=80)
        bookingTable.column("camper_size",anchor=tk.CENTER, width=80)
        bookingTable.column("date_of_booking",anchor=tk.CENTER, width=80)

        bookingTable.heading("#0",text="",anchor=tk.CENTER)
        bookingTable.heading("id",text="Booking ID",anchor=tk.CENTER)
        bookingTable.heading("camp_name",text="Camp Site",anchor=tk.CENTER)
        bookingTable.heading("region_name",text="Region",anchor=tk.CENTER)
        bookingTable.heading("camper_size",text="Camper Size",anchor=tk.CENTER)
        bookingTable.heading("date_of_booking",text="Date",anchor=tk.CENTER)

        self.dataForExport = []
        if os.path.isfile('bookingData.csv'):
            f = open('bookingData.csv', 'r', newline='', encoding='utf-8')
            reader = csv.reader(f)
            header = next(reader)
            id = 0
            for row in reader:
                bookingTable.insert(parent='',index='end',iid=id, text='',values=(row[0], row[1], row[2], row[3], row[4]))
                self.dataForExport.append(row)
                id = id+1
            f.close()

            bookingTable.pack(side=tk.TOP)
        else:
            errorLable = tk.Label(self.dialog, text="Sorry, You got no bookings!")
            errorLable.pack(side=tk.TOP, pady=(50,0))      

        self.dialog.title('Customer - Solent Campers')
        self.dialog.geometry("420x360+400+100")
        

    def exportData(self):     
        bookingList = []
        for row in self.dataForExport:
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

class AdvisorDialog:
    def __init__(self, parent):
        self.dialog = tk.Toplevel(parent)

        regionLabel = tk.Label(self.dialog, text="Select Region")
        regionLabel.pack(side=tk.TOP, pady=(20,0))

        self.region = tk.StringVar()
        self.region.set("North East")

        self.camper = tk.StringVar()
        self.camper.set("Small")

        self.camp = tk.StringVar()
        self.camp.set("")

        self.campSites = []
        self.campersType = ["Small", "Medium", "Large"]
        self.regionList = ["North East", "North West", "Yorkshire", "East Midlands", "West Midlands", "South East"]

        labelvan = tk.Label(self.dialog, text="Van Type")
        labelvan.pack(side=tk.TOP, pady=(5,0))

        optionVan = tk.OptionMenu(self.dialog, self.camper, *self.campersType)
        optionVan.pack(side=tk.TOP)

        labelregion = tk.Label(self.dialog, text="Region")
        labelregion.pack(side=tk.TOP, pady=(5,0))

        optionRegion = tk.OptionMenu(self.dialog, self.region, *self.regionList, command=self.omChanged)
        optionRegion.pack(side=tk.TOP)
        
        labelcamp = tk.Label(self.dialog, text="Camp Name")
        labelcamp.pack(side=tk.TOP, pady=(5,0))

        self.campOptionMenu = tk.OptionMenu(self.dialog, self.camp, self.campSites)   

        self.bookButton = tk.Button(self.dialog, text="Book", command=self.saveBooking)

        self.dialog.title('Advisor - Solent Campers')
        self.dialog.geometry("400x350+400+100")

    def omChanged(self, region):

        camps = []
        if not os.path.isfile('campData.csv'):
            messagebox.showerror(master=self.dialog, title="File Not Found", message="Sorry the program could not find the required files")
            return
        else:
            f = open('campData.csv', 'r')
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                if row[2] == region:
                    camps.append(row)

            f.close()

            if not len(camps) == 0:
                self.campSites = camps
                self.camp.set(camps[0][1])

                menu = self.campOptionMenu["menu"]
                menu.delete(0, "end")
                for value in self.campSites:
                    menu.add_command(label=value[1], command=lambda v=value[1]: self.camp.set(v))

                campLabel = tk.Label(self.dialog, text="Select A Camp Site")
                campLabel.pack(side=tk.TOP, pady=(20,0))

                self.campOptionMenu.pack(side=tk.TOP, pady=(0,20))
                self.bookButton.pack(side=tk.TOP)
            else:
                messagebox.showerror(master=self.dialog, title="No Sites Found", message="Couldn't Find a Camping Site Here!")
                return
        

    def saveBooking(self):
        id = random.randint(0, 50)

        if not os.path.isfile('bookingData.csv'):
            f = open('bookingData.csv', 'w', newline='', encoding='utf-8')
            csvwriter = csv.writer(f)
            csvwriter.writerow(['id', 'camp', 'region', 'camper', 'time_of_booking'])
            csvwriter.writerow([id, self.camp.get(), self.region.get(), self.camper.get(), datetime.date.today()])
            f.close()
        else:
            f = open('bookingData.csv', 'a', newline='', encoding='utf-8')
            csvwriter = csv.writer(f)
            csvwriter.writerow([id, self.camp.get(), self.region.get(), self.camper.get(), datetime.date.today()])
            f.close()

        ConfirmationDialog(self.dialog, (id, self.camp.get(), self.region.get(), self.camper.get(), datetime.date.today()))
            
class ConfirmationDialog:
    def __init__(self, parent, data):
        self.dialog = tk.Toplevel(parent) 
        self.dialog.grab_set()

        label1 = tk.Label(self.dialog, text="Booking Confirmed")
        label1.pack(side=tk.TOP)

        confirmationTable = ttk.Treeview(self.dialog)
        confirmationTable['columns'] = ('field', 'value')

        confirmationTable.column("#0", width=0,  stretch=tk.NO)
        confirmationTable.column("field", anchor=tk.CENTER, width=80)
        confirmationTable.column("value",anchor=tk.CENTER, width=80)

        confirmationTable.insert(parent='',index='end',iid=0, text='',values=("Booking ID", data[0]))
        confirmationTable.insert(parent='',index='end',iid=1, text='',values=("Camp Name", data[1]))
        confirmationTable.insert(parent='',index='end',iid=2, text='',values=("Region Name", data[2]))
        confirmationTable.insert(parent='',index='end',iid=3, text='',values=("Campter Size", data[3]))
        confirmationTable.insert(parent='',index='end',iid=4, text='',values=("Booking Date", data[4]))

        confirmationTable.pack(side=tk.TOP)

        self.dialog.title('Administrator - Solent Campers')
        self.dialog.geometry("300x350+450+100")

class AdminDialog:
    def __init__(self, parent):
        self.dialog = tk.Toplevel(parent)  

        labelCamper = tk.Label(self.dialog, text="New Camper Van.")
        labelCamper.pack(side=tk.TOP, padx=(50,10))

        label2 = tk.Label(self.dialog, text="Select Type")
        label2.pack(side=tk.TOP)

        self.camperType = tk.StringVar()
        self.camperType.set("Small")

        self.camperTypeMenu = tk.OptionMenu(self.dialog, self.camperType, *["Small", "Medium", "Large"])
        self.camperTypeMenu.pack(side=tk.TOP, pady=(0,20))

        buttonCamperAdd = tk.Button(self.dialog, text="Add New Van", height=1, width=15, command=self.addCamper)
        buttonCamperAdd.pack(side=tk.TOP)

        labelCampSite = tk.Label(self.dialog, text="New Camp Site.")
        labelCampSite.pack(side=tk.TOP, pady=(10,10))

        self.campName = tk.StringVar()
        self.campName.set("")

        self.region = tk.StringVar()
        self.region.set("North West")
        self.regionList = ["North East", "North West", "Yorkshire", "East Midlands", "West Midlands", "South East"]

        campRegionMenu = tk.OptionMenu(self.dialog, self.region, *self.regionList)
        campRegionMenu.pack(side=tk.TOP, pady=(0,5))

        label1 = tk.Label(self.dialog, text="Camp Site Name")
        label1.pack(side=tk.TOP)

        self.campNameField = tk.Entry(self.dialog, textvariable=self.campName)
        self.campNameField.pack(side=tk.TOP, pady=(00,10))       

        campSiteAddButton = tk.Button(self.dialog, text="Add Site", height=1, width=15, command=self.addCampSite)
        campSiteAddButton.pack(side=tk.TOP)

        self.dialog.title('Administrator - Solent Campers')
        self.dialog.geometry("400x350+450+100")
     

    def addCamper(self):
        id = random.randint(1,20)
        header = ['id', 'size']

        if not os.path.isfile('camperData.csv'):
            f = open('camperData.csv', 'w', newline='', encoding='utf-8')
            csvwriter = csv.writer(f)
            csvwriter.writerow(header)
            csvwriter.writerow([id, self.camperType.get()])
            f.close()
        else:
            f = open('camperData.csv', 'a', newline='', encoding='utf-8')
            csvwriter = csv.writer(f)
            csvwriter.writerow([id, self.camperType.get()])
            f.close()
            
        messagebox.showinfo(master=self.dialog, title="New Camper Added", message="Camper ID: " + str(id) +  " Camper Size: " + self.camperType.get())

    def addCampSite(self):
        id = random.randint(1,50)
        header = ['id', 'camp', 'region']

        if not os.path.isfile('campData.csv'):
            f = open('campData.csv', 'w', newline='', encoding='utf-8')
            csvwriter = csv.writer(f)
            csvwriter.writerow(header)
            csvwriter.writerow([id, self.campName.get(), self.region.get()])
            f.close()
        else:
            f = open('campData.csv', 'a', newline='', encoding='utf-8')
            csvwriter = csv.writer(f)
            csvwriter.writerow([id, self.campName.get(), self.region.get()])
            f.close()
            
        messagebox.showinfo(master=self.dialog, title="New Camp Site Added", message="Camp Site ID: " + str(id) +  " Camp Site Name: " + self.campName.get() +  " Region Name: " + self.region.get())