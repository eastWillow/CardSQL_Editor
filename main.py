# -*- coding: UTF-8 -*-
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import sqlite3
from tkinter import ttk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        frame1 = tk.Frame(self)
        self.step1 = tk.Button(frame1)
        self.step1["text"] = "選擇牌組資料庫開啟\n(STEP1)"
        self.step1["command"] = self.say_hi
        self.step1.pack(side="left")
        ##
        self.step1_label = tk.Label(frame1)
        self.step1_label["text"] = "X"
        self.step1_label.pack(side="right")
        ##
        frame1.pack(side="top")
        ##
        self.select_role_label = tk.Label(self)
        self.select_role_label["text"] = "選擇規則\n(STEP2)"
        self.select_role_label.pack(side="top")
        ##
        self.comboExample = ttk.Combobox(self, 
                            values=[
                                    "請選擇目標規則(0)",
                                    "OCG專有(1)", 
                                    "TCG專有(2)",
                                    "OCG&TCG(3)",
                                    "Anime/DIY(4)"])
        self.comboExample.current(0)
        self.comboExample.pack(side="top")
        ##
        self.check_button = tk.Button(self)
        self.check_button["text"] = "檢查選擇到的卡片\n(STEP3)"
        self.check_button["command"] = self.pop_up_check_card_list
        self.check_button.pack(side="top")
        ##
        self.newRule_label = tk.Label(self)
        self.newRule_label["text"] = "請選擇取代後規則\n(STEP4)"
        self.newRule_label.pack(side="top")
        ##
        self.newRule = ttk.Combobox(self, 
                            values=[
                                    "請選擇取代後規則(0)",
                                    "OCG專有(1)", 
                                    "TCG專有(2)",
                                    "OCG&TCG(3)",
                                    "Anime/DIY(4)"])
        self.newRule.current(0)
        self.newRule.pack(side="top")
        ##
        self.update_rule_button = tk.Button(self)
        self.update_rule_button["text"] = "取代規則\n(STEP5)"
        self.update_rule_button["command"] = self.update_rule
        self.update_rule_button.pack(side="top")
        ##
        self.quit = tk.Button(self, text="離開", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")
        
    def say_hi(self):
        root.filename =  filedialog.askopenfilename(parent=root,filetypes=[('牌組資料庫', '.cdb')],title=u'選擇牌組資料庫開啟')
        root.conn = sqlite3.connect(root.filename)
        self.step1_label["text"] = "V"
        
    def pop_up_check_card_list(self):        
        if hasattr(root, 'conn') and (self.comboExample.current()!= 0):
            
            self.popup = tk.Tk()
            self.popup.wm_title("List")

            B1 = tk.Button(self.popup, text="離開", fg="red", command = self.popup.destroy)
            B1.pack()
            
            label = ttk.Label(self.popup, text="卡片清單")
            label.pack(side="top", fill="x",expand=1)

            frame = tk.Frame(self.popup)
            self.listNodes = tk.Listbox(frame, width=20, height=20, font=("Helvetica", 12))
            self.listNodes.pack(side="left",fill="y")
            self.scrollbar = tk.Scrollbar(frame, orient="vertical")
            self.scrollbar.config(command=self.listNodes.yview)
            self.scrollbar.pack(side="left",fill="y")
            self.listNodes.config(yscrollcommand=self.scrollbar.set)
            frame.pack()
        
            cur = root.conn.cursor()
            cur.execute("SELECT `name` FROM `texts` WHERE `id` IN (SELECT `id` FROM `datas` WHERE `ot` LIKE '{0}')".format(self.comboExample.current()))
            rows = cur.fetchall()
        
            for row in rows:
                self.listNodes.insert(tk.END, str(row[0]))

        else:
            messagebox.showerror("Error", "請按照步驟執行")
    
    def update_rule(self):        
        if hasattr(root, 'conn') and (self.comboExample.current()!= 0):
            cur = root.conn.cursor()
            cur.execute("UPDATE `datas` SET `ot`='{1}' WHERE `ot`='{0}'".format(self.comboExample.current(),self.newRule.current()))
            root.conn.commit()
            messagebox.showinfo("提示","更新完成")
        else:
            messagebox.showerror("錯誤", "請按照步驟執行")
            
root = tk.Tk()
root.geometry("680x500")
app = Application(master=root)
app.mainloop()

if hasattr(root, 'conn'):
    root.conn.close()
