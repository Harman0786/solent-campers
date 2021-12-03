import tkinter as tk

class Main:
    def __init__(self):
        self.root = tk.Tk()

        label1 = tk.Label(self.root, text="Solent Campers!")
        label1.pack(side=tk.TOP, pady=(20,0))

        label1 = tk.Label(self.root, text="One Stop for All Campers")
        label1.pack(side=tk.TOP, pady=(20,0))

        button1 = tk.Button(self.root, text="Customer", height=3, width=15, command=self.cutomerDialog)
        button1.pack(side=tk.TOP, pady=(10, 10))

        button2 = tk.Button(self.root, text="Advisor", height=3, width=15, command=self.advisorDialog)
        button2.pack(side=tk.TOP, pady=(10, 10))

        button3 = tk.Button(self.root, text="Admin", height=3, width=15, command=self.adminDialog)
        button3.pack(side=tk.TOP, pady=(10, 10))

        self.root.title('Solent Campers - COM 714')
        self.root.geometry("250x350+200+250")

    def advisorDialog(self):
        pass
    def adminDialog(self):
        pass

    def cutomerDialog(self):
        pass

app = Main()
app.root.mainloop()