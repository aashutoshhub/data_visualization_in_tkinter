
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from tkinter import*
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
from webbrowser import BackgroundBrowser
import matplotlib.pyplot as plt
import pandas as pd

from PIL import Image,ImageTk
from sklearn.neighbors import radius_neighbors_graph 


root = tk.Tk()

root.geometry("800x600")
root.pack_propagate(False) 
root.resizable(0, 0) 

#image in background
image=Image.open("dv2.jpg")
photo=ImageTk.PhotoImage(image)

lbl=Label(root,image=photo)
lbl.pack(pady=0,padx=0)


frame1 = tk.LabelFrame(root, text="Excel Data",bg="green")
frame1.place(height=250, width=600,rely=0.15,relx=0.12)


file_frame = tk.LabelFrame(root, text="Open File",bg="green")
file_frame.place(height=100, width=400, rely=0.75, relx=0.21)


button1 = tk.Button(file_frame, text="Browse A File",bg="#8083d9", command=lambda: File_dialog())
button1.place(rely=0.65, relx=0.50)

button2 = tk.Button(file_frame, text="Load File",bg="#5f3ec2" ,command=lambda: Load_excel_data())
button2.place(rely=0.65, relx=0.30)


label_file = ttk.Label(file_frame, text="No File Selected")
label_file.place(rely=0, relx=0)

style=ttk.Style()
style.theme_use("alt")
style.configure("Treeview",
                background="#356ef2",
                foreground="black",
                rowheight=25,
                fieldbackground="silver"   
                )
style.map('Treeview',
          background=[('selected','#14d9cc')])

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
                                          filetype=(('csv Files', '*.csv'),("xlsx files", "*.xlsx"),("All Files", "*.*")))
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
            # image=Image.open()
            # photo=ImageTk.PhotoImage(image)

            # lbl=Label(root,image=photo)
            # lbl.pack(pady=0,padx=0)
    
    
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
  
        submit = Button(root,text = "Bar graph",command = bargraph).place(x=160,y=380)
        submit = Button(root, text = "pie chart",command = piechart).place(x=330,y=380)
        submit = Button(root, text = "line graph",command = linegraph).place(x=490,y=380)
       

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