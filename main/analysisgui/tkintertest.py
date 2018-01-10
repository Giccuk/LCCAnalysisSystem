import tkinter as tk
from show import *
import sys

sys.path.insert(0,'/Users/cancui/workspace/anaconda3/envs/abiba_analysis/src/main/AnalysisSystem/')

from mldatatest import get_interdata_mysql

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        # hi button
        self.hi_button = tk.Button(self)
        self.hi_button["text"] = "Hello World\n(click me)"
        self.hi_button["command"] = self.say_hi
        self.hi_button.pack(side="bottom")
        # quit button
        self.quit_button = tk.Button(self, text="QUIT",fg="red", command=root.destroy)
        self.quit_button.pack(side="bottom")
        #role_button
        self.role_button=tk.Button(self,text="Role Selection",command=self.select_role)
        self.role_button.pack(side="bottom")
        #show_name_button
        self.showname_button=tk.Button(self,text="show name",command=get_name(4))
        self.role_button.pack(side="bottom")
        #show_interid_button
        self.show_interid_button=tk.Button(self,text="show interid button",command=self.show_interdata)
        self.show_interid_button.pack(side="bottom")

        self.role_blank=tk.Entry(self)
        self.role_blank["show"]='*'
        self.role_blank.pack()

        self.show_box=tk.Text(self)
        self.show_box.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

    def select_role(self):
        role=input("Please type in the a role from 'proposer' and 'responder':")
        print(role)
        if role=='proposer':
            print("you choose to be a proposer")
        else:
            print("you choose to be a responder")

    def show_interdata(self):
        var=get_interdata_mysql('lccgame')
        self.show_box.insert('end',var[0])



root = tk.Tk()
root.geometry("200x200")
app = Application(root)
app.mainloop()

