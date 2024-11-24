from tkinter import *
from backend import predict_smoker
from tkinter import ttk, messagebox
import mysql.connector

#Functions
def submit_data():
    field_values=[]
    field_values.append(gender_entry.get())
    field_values.append(age_entry.get())
    field_values.append(height_entry.get())
    field_values.append(weight_entry.get())
    field_values.append(waist_entry.get())
    field_values.append(systolic_entry.get())
    field_values.append(fasting_entry.get())
    field_values.append(cholesterol_entry.get())
    field_values.append(triglyceride_entry.get())
    field_values.append(ldl_entry.get())
    field_values.append(hemoglobin_entry.get())
    field_values.append(creatinine_entry.get())
    field_values.append(ast_entry.get())
    field_values.append(alt_entry.get())
    field_values.append(gtp_entry.get())
    field_values.append(oral_entry.get())
    field_values.append(dental_caries_entry.get())
    field_values.append(tartar_entry.get())
    
    output = predict_smoker(field_values)
    if output == 0:
        output = "Non-smoker"
    else:
        output = "Smoker"
    txtSmokingStatus.insert(END, "\n" + output)
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="mydata")
    mycursor = mysqldb.cursor()
    try:
        sql = "INSERT INTO smoker(id, gender, age, height_cm, weight_kg, waist_cm, systolic, fasting_blood_sugar, Cholesterol, triglyceride, LDL, hemoglobin, serum_creatinine, AST, ALT, Gtp, oral, dental_caries, tartar, smoking) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (id_entry.get(), gender_entry.get(), age_entry.get(), height_entry.get(), weight_entry.get(),waist_entry.get(),systolic_entry.get(),fasting_entry.get(),cholesterol_entry.get(),triglyceride_entry.get(),ldl_entry.get(),hemoglobin_entry.get(),creatinine_entry.get(),ast_entry.get(),alt_entry.get(),gtp_entry.get(),oral_entry.get(),dental_caries_entry.get(),tartar_entry.get(),output)
        mycursor.execute(sql,val)
        mysqldb.commit()
        lastid = mycursor.lastrowid
        messagebox.showinfo("Information","Record Inserted Successfully!")
    except Exception as e:
        print(e) 
        mysqldb.rollback()
        mysqldb.close()

def delete_row():
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="mydata")
    mycursor = mysqldb.cursor()

    try: 
        sql = "DELETE from smoker where id = %s"
        val = (id_entry.get(),)
        mycursor.execute(sql,val)
        mysqldb.commit()
        lastid = mycursor.lastrowid
        messagebox.showinfo("Information","Record Deleted Successfully!")
    except Exception as e:
        print(e) 
        mysqldb.rollback()
        mysqldb.close()

def GetValue(event):
    row_id = listBox.selection()[0]
    select = listBox.set(row_id)
    id_entry.insert(0,select['id'])
    
def show():
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="mydata")
    mycursor = mysqldb.cursor()
    mycursor.execute("SELECT id, gender, age, height_cm, weight_kg, waist_cm, systolic, fasting_blood_sugar, Cholesterol, triglyceride, LDL, hemoglobin, serum_creatinine, AST, ALT, Gtp, oral, dental_caries, tartar, smoking FROM smoker; ")
    records = mycursor.fetchall()
    print(records)
    for i , (id, gender, age, height_cm, weight_kg, waist_cm, systolic, fasting_blood_sugar, Cholesterol, triglyceride, LDL, hemoglobin, serum_creatinine, AST, ALT, Gtp, oral, dental_caries, tartar, smoking) in enumerate(records, start=1):
        listBox.insert("", "end", values=(id, gender, age, height_cm, weight_kg, waist_cm, systolic, fasting_blood_sugar, Cholesterol, triglyceride, LDL, hemoglobin, serum_creatinine, AST, ALT, Gtp, oral, dental_caries, tartar, smoking))
        listBox.pack()
        mysqldb.close()


root = Tk()
root.title("Smoking Detection System")
root.geometry("1540x800+0+0")

lbltitle = Label(root, bd=20, relief=RIDGE, text="Smoking Detection System", fg="white", bg="black",
                    font=("times new roman", 50, "bold"))
lbltitle.grid(row=0, column=1)

# Dataframe
Dataframe = Frame(root, bd=20, relief=RIDGE)
Dataframe.place(x=0, y=130, width=1365, height=360)

DataframeLeft = LabelFrame(Dataframe, bd=10, padx=20, relief=RIDGE, font=("times new roman", 18, "bold"),
                            text="Patient Information")
DataframeLeft.place(x=0, y=5, width=980, height=320)

DataframeRight = LabelFrame(Dataframe, bd=10, padx=20, relief=RIDGE, font=("times new roman", 18, "bold"),
                            text="Smoking Status")
DataframeRight.place(x=990, y=5, width=330, height=320)

# Button Frame
Buttonframe = Frame(root, bd=20, relief=RIDGE)
Buttonframe.place(x=0, y=500, width=1365, height=70)

# Details Frame
Detailsframe = Frame(root, bd=20, relief=RIDGE)
Detailsframe.place(x=0, y=580, width=1370, height=150)

# Data Frame Level Fields
oral_entry = StringVar()
gender_entry = StringVar()
dental_caries_entry = StringVar()
tartar_entry = StringVar()

# Create the radio button fields
gender_label = Label(DataframeLeft, text="Gender:", font=("arial", 10))
gender_label.grid(row=0, column=5, padx=2, pady=6, sticky=W)
gender_male = Radiobutton(DataframeLeft, text="Male", variable=gender_entry, value="1")
gender_male.grid(row=0, column=6, padx=2, pady=6)
gender_female = Radiobutton(DataframeLeft, text="Female", variable=gender_entry, value="0")
gender_female.grid(row=0, column=7, padx=2, pady=6)

oral_label = Label(DataframeLeft, text="Oral:",font=("arial", 10))
oral_label.grid(row=1, column=5, padx=2, pady=6, sticky=W)
oral_yes = Radiobutton(DataframeLeft, text="Yes", variable=oral_entry, value="1")
oral_yes.grid(row=1, column=6, padx=2, pady=6)
oral_no = Radiobutton(DataframeLeft, text="No", variable=oral_entry, value="0")
oral_no.grid(row=1, column=7, padx=2, pady=6)

dental_caries_label = Label(DataframeLeft, text="Dental Caries:",font=("arial", 10))
dental_caries_label.grid(row=2, column=5, padx=2, pady=6, sticky=W)
dental_caries_yes = Radiobutton(DataframeLeft, text="Yes", variable=dental_caries_entry, value="1")
dental_caries_yes.grid(row=2, column=6, padx=2, pady=6)
dental_caries_no = Radiobutton(DataframeLeft, text="No", variable=dental_caries_entry, value="0")
dental_caries_no.grid(row=2, column=7, padx=2, pady=6)

tartar_label = Label(DataframeLeft, text="Tartar:", font=("arial", 10))
tartar_label.grid(row=3, column=5, padx=2, pady=6, sticky=W)
tartar_yes = Radiobutton(DataframeLeft, text="Yes", variable=tartar_entry, value="1")
tartar_yes.grid(row=3, column=6, padx=2, pady=6)
tartar_no = Radiobutton(DataframeLeft, text="No", variable=tartar_entry, value="0")
tartar_no.grid(row=3, column=7, padx=2, pady=6)

id_label = Label(DataframeLeft, text="Patient ID:",padx=2, pady=6,font=("arial", 12))
id_label.grid(row=0, column=0)
age_label = Label(DataframeLeft, text="Age:",padx=2, pady=6,font=("arial", 12))
age_label.grid(row=1, column=0)
height_label = Label(DataframeLeft, text="Height (cm):",padx=2, pady=6,font=("arial", 12))
height_label.grid(row=2, column=0)
weight_label = Label(DataframeLeft, text="Weight (kg):",padx=2, pady=6,font=("arial", 12))
weight_label.grid(row=3, column=0)
waist_label = Label(DataframeLeft, text="Waist (cm):",padx=2, pady=6,font=("arial", 12))
waist_label.grid(row=4, column=0)
systolic_label = Label(DataframeLeft, text="Systolic:",padx=2, pady=6,font=("arial", 12))
systolic_label.grid(row=5, column=0)
fasting_label = Label(DataframeLeft, text="Fasting Blood Sugar:",padx=2, pady=6,font=("arial", 12))
fasting_label.grid(row=6, column=0)
cholesterol_label = Label(DataframeLeft, text="Cholesterol:",padx=2, pady=6,font=("arial", 12))
cholesterol_label.grid(row=7, column=0)
triglyceride_label = Label(DataframeLeft, text="Triglyceride:",padx=2, pady=6,font=("arial", 12))
triglyceride_label.grid(row=0, column=2)
ldl_label = Label(DataframeLeft, text="LDL:",padx=2, pady=6,font=("arial", 12))
ldl_label.grid(row=1, column=2)
hemoglobin_label = Label(DataframeLeft, text="Hemoglobin:",padx=2, pady=6,font=("arial", 12))
hemoglobin_label.grid(row=2, column=2)
creatinine_label = Label(DataframeLeft, text="Serum Creatinine:",padx=2, pady=6,font=("arial", 12))
creatinine_label.grid(row=3, column=2)
ast_label = Label(DataframeLeft, text="AST:",padx=2, pady=6,font=("arial", 12))
ast_label.grid(row=4, column=2)
alt_label = Label(DataframeLeft, text="ALT:",padx=2, pady=6,font=("arial", 12))
alt_label.grid(row=5, column=2)
gtp_label = Label(DataframeLeft, text="GTP:",padx=2, pady=6,font=("arial", 12))
gtp_label.grid(row=6, column=2)

# Create entry fields for each input
id_entry = Entry(DataframeLeft, font=("arial", 10), textvariable = StringVar())
id_entry.grid(row=0, column=1)
age_entry = Entry(DataframeLeft, font=("arial", 10), textvariable = StringVar())
age_entry.grid(row=1, column=1)
height_entry = Entry(DataframeLeft, font=("arial", 10), textvariable = StringVar())
height_entry.grid(row=2, column=1)
weight_entry = Entry(DataframeLeft, font=("arial", 10), textvariable = StringVar())
weight_entry.grid(row=3, column=1)
waist_entry = Entry(DataframeLeft, font=("arial", 10), textvariable = StringVar())
waist_entry.grid(row=4, column=1)
systolic_entry = Entry(DataframeLeft, font=("arial", 10), textvariable = StringVar())
systolic_entry.grid(row=5, column=1)
fasting_entry = Entry(DataframeLeft, font=("arial", 10), textvariable = StringVar())
fasting_entry.grid(row=6, column=1)
cholesterol_entry = Entry(DataframeLeft, font=("arial", 10), textvariable = StringVar())
cholesterol_entry.grid(row=7, column=1)
triglyceride_entry = Entry(DataframeLeft, font=("arial", 10), textvariable = StringVar())
triglyceride_entry.grid(row=0, column=3)
ldl_entry = Entry(DataframeLeft, font=("arial", 10), textvariable = StringVar())
ldl_entry.grid(row=1, column=3)
hemoglobin_entry = Entry(DataframeLeft, font=("arial", 10), textvariable = StringVar())
hemoglobin_entry.grid(row=2, column=3)
creatinine_entry = Entry(DataframeLeft, font=("arial", 10), textvariable = StringVar())
creatinine_entry.grid(row=3, column=3)
ast_entry = Entry(DataframeLeft, font=("arial", 10), textvariable = StringVar())
ast_entry.grid(row=4, column=3)
alt_entry = Entry(DataframeLeft, font=("arial", 10), textvariable = StringVar())
alt_entry.grid(row=5, column=3)
gtp_entry = Entry(DataframeLeft, font=("arial", 10), textvariable = StringVar())
gtp_entry.grid(row=6, column=3)

# Data Frame Right
txtSmokingStatus = Text(DataframeRight, font=("times new roman", 18, "bold"), width=23, height=10, padx=2, pady=6)
txtSmokingStatus.grid(row=0, column=0)

# Buttons
btnSubmit = Button(Buttonframe,command=submit_data,text="Submit",bg="white",fg="black",font=("arial", 12, "bold"),width=16, height=1, padx=2, pady=6)
btnSubmit.grid(row=0, column=0)
btnDelete = Button(Buttonframe,command=delete_row,text="Delete",bg="white",fg="black",font=("arial", 12, "bold"),width=16, height=1, padx=2, pady=6)
btnDelete.grid(row=0, column=2)

# Database Table
cols = ('id','gender', 'age', 'height(cm)', 'weight(kg)', 'waist(cm)', 'systolic',
       'fasting blood sugar', 'Cholesterol', 'triglyceride', 'LDL',
       'hemoglobin', 'serum creatinine', 'AST', 'ALT', 'Gtp', 'oral',
       'dental caries', 'tartar','smoking')

listBox = ttk.Treeview(Detailsframe, columns=cols, show='headings')
listBox.column("# 1", anchor=CENTER, stretch=NO, width="65")
listBox.column("# 2", anchor=CENTER, stretch=NO, width="65")
listBox.column("# 3", anchor=CENTER, stretch=NO, width="65")
listBox.column("# 4", anchor=CENTER, stretch=NO, width="65")
listBox.column("# 5", anchor=CENTER, stretch=NO, width="65")
listBox.column("# 6", anchor=CENTER, stretch=NO, width="65")
listBox.column("# 7", anchor=CENTER, stretch=NO, width="65")
listBox.column("# 8", anchor=CENTER, stretch=NO, width="65")
listBox.column("# 9", anchor=CENTER, stretch=NO, width="65")
listBox.column("# 10", anchor=CENTER, stretch=NO, width="65")
listBox.column("# 11", anchor=CENTER, stretch=NO, width="65")
listBox.column("# 12", anchor=CENTER, stretch=NO, width="65")
listBox.column("# 13", anchor=CENTER, stretch=NO, width="65")
listBox.column("# 14", anchor=CENTER, stretch=NO, width="65")
listBox.column("# 15", anchor=CENTER, stretch=NO, width="65")
listBox.column("# 16", anchor=CENTER, stretch=NO, width="65")
listBox.column("# 17", anchor=CENTER, stretch=NO, width="65")
listBox.column("# 18", anchor=CENTER, stretch=NO, width="65")
listBox.column("# 19", anchor=CENTER, stretch=NO, width="65")
listBox.column("# 20", anchor=CENTER, stretch=NO, width="80")

for col in cols:
    listBox.heading(col, text=col)
    listBox.grid(row=1,column=0)

show()
listBox.bind('<Double-Button-1>', GetValue)

root.mainloop()