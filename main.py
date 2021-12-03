import tkinter as tk
import tkinter.ttk as ttk
from dialogs import CustomerDialog, AdvisorDialog, AdminDialog

class Main:
    def __init__(self):
        self.root = tk.Tk()
        s=ttk.Style()
        s.theme_use('classic')

        label1 = tk.Label(self.root, text="Solent Campers!")
        label1.pack(side=tk.TOP, pady=(20,0))

        label1 = tk.Label(self.root, text="One Stop for All Campers")
        label1.pack(side=tk.TOP, pady=(20,0))

        button1 = tk.Button(self.root, text="Customer", height=3, width=15, bg='orange', command=self.cutomerDialog)
        button1.pack(side=tk.TOP, pady=(10, 10))

        button2 = tk.Button(self.root, text="Advisor", height=3, width=15, bg='green', command=self.advisorDialog)
        button2.pack(side=tk.TOP, pady=(10, 10))

        button3 = tk.Button(self.root, text="Admin", height=3, width=15, bg='red', command=self.adminDialog)
        button3.pack(side=tk.TOP, pady=(10, 10))

        self.root.title('Solent Campers - COM 714')
        self.root.geometry("250x350+200+250")

    def advisorDialog(self):
        advisorDialog = AdvisorDialog(self.root)
        advisorDialog.dialog.mainloop()
    def adminDialog(self):
        adminDialog = AdminDialog(self.root)
        adminDialog.dialog.mainloop()

    def cutomerDialog(self):
        customerDialog = CustomerDialog(self.root)
        customerDialog.dialog.mainloop()

app = Main()
app.root.mainloop()