
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from tkinter import*
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
import matplotlib.pyplot as plt
import pandas as pd


root = tk.Tk()

root.geometry("500x500")
root.pack_propagate(False) 
root.resizable(0, 0) 


frame1 = tk.LabelFrame(root, text="Excel Data")
frame1.place(height=250, width=500)


file_frame = tk.LabelFrame(root, text="Open File")
file_frame.place(height=100, width=400, rely=0.65, relx=0)


button1 = tk.Button(file_frame, text="Browse A File", command=lambda: File_dialog())
button1.place(rely=0.65, relx=0.50)

button2 = tk.Button(file_frame, text="Load File", command=lambda: Load_excel_data())
button2.place(rely=0.65, relx=0.30)


label_file = ttk.Label(file_frame, text="No File Selected")
label_file.place(rely=0, relx=0)



tv1 = ttk.Treeview(frame1)
tv1.place(relheight=1, relwidth=1) 

treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview) 
treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview) 
tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) 
treescrollx.pack(side="bottom", fill="x") 
treescrolly.pack(side="right", fill="y")


def File_dialog():
    
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select A File",
                                          filetype=(("xlsx files", "*.xlsx"),('csv Files', '*.csv'),("All Files", "*.*")))
    label_file["text"] = filename
    return None


def Load_excel_data():
   
    file_path = label_file["text"]
    try:
        excel_filename = r"{}".format(file_path)
        if excel_filename[-4:] == ".csv":
            df = pd.read_csv(excel_filename)
            x=df['Country']
            y=df['Active']
        else:
            df = pd.read_excel(excel_filename)
            x=df['Country']
            y=df['Active']
        
        plt.style.use('bmh')

        def bargraph():
            plt.clf()
            plt.xlabel('Country',fontsize=18)
            plt.ylabel('Active',fontsize=18)
            plt.bar(x,y)
            plt.show()
    
    
        # Pie chart
        def piechart():
            plt.clf()
            plt.pie(y, labels=x, radius=1,autopct='%0.01f%%', shadow=True)
            plt.show()
    
        def linegraph():
            # Line Graph
            plt.clf()
            plt.xlabel('Country',fontsize=18)
            plt.ylabel('Active',fontsize=18)
            plt.scatter(x, y)
            plt.plot(x, y) 
            plt.show()
    
        submit = Button(root,text = "Bar graph",command = bargraph).place(x=50,y=280)
        submit = Button(root, text = "pie chart",command = piechart).place(x=150,y=280)
        submit = Button(root, text = "line graph",command = linegraph).place(x=250,y=280) 

    except ValueError:
        tk.messagebox.showerror("Information", "The file you have chosen is invalid")
        return None
    except FileNotFoundError:
        tk.messagebox.showerror("Information", f"No such file as {file_path}")
        return None

    clear_data()
    tv1["column"] = list(df.columns)
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column)

    df_rows = df.to_numpy().tolist() 
    for row in df_rows:
        tv1.insert("", "end", values=row) 
    return None




def clear_data():
    tv1.delete(*tv1.get_children())
    return None


root.mainloop()