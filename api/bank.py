import tabula
import pandas as pd

#from PyPDF2 import PdfFileReader
import re
import pdftotext

import fitz
import json
# SBI Bank Module
def bank_details_sbi(filename):
    #pdf_path3 = "text2.pdf"
    dfs = tabula.read_pdf(filename, pages = "all")
    tabula.convert_into(filename, "output.csv", output_format="csv", pages='all')
    #pdf_path=r"text2.pdf"

    df = pd.read_csv("output.csv", thousands=",")

    debit = df["Debit"]
    credit = df["Credit"]
    bal = df["Balance"]

    t_debit = debit.sum(skipna=True)
    t_credit = credit.sum(skipna=True)
    t_bal = bal.sum(skipna=True)

    """
        Whole List of stuffs
    """
    bank_text = []


# Load your PDF
    with open(filename, "rb") as f:
        pdf = pdftotext.PDF(f)

    # If it's password-protected
    #with open("secure.pdf", "rb") as f:
    #    pdf = pdftotext.PDF(f, "secret")

    # How many pages?
    #print(len(pdf))

    # Iterate over all the pages
    #for page in pdf:
    #    print(page)

    data = "\n\n".join(pdf)
    # Read all the text into one string
    #print(data)
    acc_name= " " + '\n'.join([re.sub(r'Account Name\s+:', '', line) for line in data.splitlines() if 'Account Name' in line])
    acc_no= " "+ '\n'.join([re.sub(r'Account Number\s+:', '', line) for line in data.splitlines() if 'Account Number' in line])
    acc_code = " "+ '\n'.join([re.sub(r'IFS Code\s+:', '', line) for line in data.splitlines() if 'IFS Code' in line])
    
    op_bal = " " + str(bal[df["Balance"].first_valid_index()])
    cl_bal = " " + str(bal[df["Balance"].last_valid_index()])
    t_debit = " " + str(t_debit)
    t_credit = " " + str(t_credit)
    t_bal = " " + str(t_bal)
    print(acc_name,"\n",acc_code,"\n",acc_no,"\n",op_bal,"\n",cl_bal)
    bank_text.append(acc_no)
    bank_text.append(acc_name)
    bank_text.append(acc_code)
    
    bank_text.append(op_bal)
    bank_text.append(cl_bal)

    bank_text.append(t_debit)
    bank_text.append(t_credit)
    bank_text.append(t_bal)
    print(bank_text, "XXX")
    print("\n")
    expense_report = []
    expenses = df.iloc[:][['Description','Debit']].dropna()
    bank_text.append(expenses)
    incomes = df.iloc[:][['Description','Credit']].dropna()
    bank_text.append(incomes)
    #logo(filename)
    #print(f"Total Debit:%.2f \nTotal Credit:%.2f \nTotal Balance:%.2f" % (t_debit, t_credit, t_bal) )
    json_result = {
        "Account Number" : bank_text[0],
        "Account Name" : bank_text[1],
        "IFSC Code": bank_text[2],
        "Opening Balance": bank_text[3],
        "Closing Balance": bank_text[4],
        "Total Debit Summary": bank_text[5],
        "Total Credit Summary": bank_text[6],
        "Total Balance Summary": bank_text[7],

        #"Expenses": bank_text[8],
        #"Incomes": bank_text[9]
    }
    return json_result #bank_text

# Allahabad bank module

def bank_details_alla(filename):
    #pdf_path3 = "text2.pdf"
    dfs = tabula.read_pdf(filename, pages = "all")
    tabula.convert_into(filename, "output.csv", output_format="csv", pages='all')
    #pdf_path=r"text2.pdf"

    df = pd.read_csv("output.csv", thousands=",", error_bad_lines=False)

    debit = df["DR"].dropna()
    credit = df["CR"].dropna()
    df["Balance"] = df["Balance"].str.strip(" CR")
    bal = df["Balance"]
    print(bal, "XXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    debit = pd.to_numeric(df["DR"], errors = 'coerce')
    credit = pd.to_numeric(df["CR"], errors = 'coerce')
    bal = pd.to_numeric(df["Balance"], errors = 'coerce')
    #debit = debit.astype(float)
    #credit = credit.astype(float)262603
    t_debit = debit.sum(skipna=True)
    t_credit = credit.sum(skipna=True)
    t_bal = bal.sum()

    """coerce
        Whole List of stuffs
    """
    bank_text = []


# Load your PDF
    with open(filename, "rb") as f:
        pdf = pdftotext.PDF(f)

    # If it's password-protected
    #with open("secure.pdf", "rb") as f:
    #    pdf = pdftotext.PDF(f, "secret")

    # How many pages?
    #print(len(pdf))

    # Iterate over all the pages
    #for page in pdf:
    #    print(page)
    #print(bal)
    data = "\n\n".join(pdf)
    # Read all the text into one string
    #print(data)
    acc_name= ' '.join([re.sub(r'^[\d \t]+|[\d \t]+:$', '', line) for line in data.splitlines() if 'Mr. ' in line])
    acc_no= ' '.join([re.sub(r'Account Number\s+:', '', line) for line in data.splitlines() if 'Account Number' in line])
    acc_code = ' '.join([re.sub(r'IFSC Code\s+:', '', line) for line in data.splitlines() if 'IFSC Code' in line])
    op_bal = " " + str(bal[df["Balance"].first_valid_index()])
    cl_bal = " " + str(bal[df["Balance"].last_valid_index()])
    t_debit = " " + str(t_debit)
    t_credit = " " + str(t_credit)
    t_bal = " " + str(t_bal)
    
    bank_text.append(acc_no)
    bank_text.append(acc_name)
    bank_text.append(acc_code)
    
    bank_text.append(op_bal)
    bank_text.append(cl_bal)

    bank_text.append(t_debit)
    bank_text.append(t_credit)
    bank_text.append(t_bal)

    expenses = df.iloc[:][['Description','DR']].dropna()
    bank_text.append(expenses)
    incomes = df.iloc[:][['Description','CR']].dropna()
    bank_text.append(incomes)
    #print(bank_text, "XXX")
    #print("\n")
    
    #logo(filename)
    #print(f"Total Debit:%.2f \nTotal Credit:%.2f \nTotal Balance:%.2f" % (t_debit, t_credit, t_bal) )
    json_result = {
        "Account Number" : bank_text[0],
        "Account Name" : bank_text[1],
        "IFSC Code": bank_text[2],
        "Opening Balance": bank_text[3],
        "Closing Balance": bank_text[4],
        "Total Debit Summary": bank_text[5],
        "Total Credit Summary": bank_text[6],
        "Total Balance Summary": bank_text[7],

        #"Expenses": bank_text[8],
        #"Incomes": bank_text[9]
    }
    return json_result

# YES Bank Module

def bank_details_yes(filename):
    #pdf_path3 = "text2.pdf"
    dfs = tabula.read_pdf(filename, pages = "all")
    tabula.convert_into(filename, "output.csv", output_format="csv", pages='1')
    #pdf_path=r"text2.pdf"

    df = pd.read_csv("output.csv", thousands=",",error_bad_lines=False)

    debit = df["Debit"].dropna().reset_index(drop=True)
    credit = df["Credit"].dropna().reset_index(drop=True)
    bal = df["Balance"].dropna().reset_index(drop=True)

    t_debit = debit.sum(skipna=True)
    t_credit = credit.sum(skipna=True)
    t_bal = bal.sum(skipna=True)
    # print(t_bal, "XYYY")
    """
        Whole List of stuffs
    """
    bank_text = []


# Load your PDF
    with open(filename, "rb") as f:
        pdf = pdftotext.PDF(f)

    # If it's password-protected
    #with str many pages?
    #print(len(pdf))

    # Iterate over all the pages
    #for page in pdf:
    #    print(page)

    data = "\n\n".join(pdf)
    # Read all the text into one string
    #print(data)
    acc_name= " " + '\n'.join([re.sub(r'^[\d \t]+|[\d \t]+$', '', line) for line in data.splitlines() if 'MRS.' in line])
    acc_no= " "+ '\n'.join([re.sub(r'ACCOUNT No.\s+:', '', line) for line in data.splitlines() if 'ACCOUNT No.' in line])
    acc_code = " "+ '\n'.join([re.sub(r'IFSC Code\s+:', '', line) for line in data.splitlines() if 'IFSC' in line])
    
    op_bal = " " + str(bal[0])
    cl_bal = " " + str(bal[(len(bal)-1)])
    t_debit = " " + str(t_debit)
    t_credit = " " + str(t_credit)
    t_bal = " " + str(t_bal)
    #print(acc_name,"\n",acc_code,"\n",acc_no,"\n",op_bal,"\n",cl_bal)
    bank_text.append(acc_no)
    bank_text.append(acc_name)
    bank_text.append(acc_code)
    
    bank_text.append(op_bal)
    bank_text.append(cl_bal)

    bank_text.append(t_debit)
    bank_text.append(t_credit)
    bank_text.append(t_bal)

    expenses = df.iloc[:][['Description','Debit']].dropna()
    bank_text.append(expenses)
    incomes = df.iloc[:][['Description','Credit']].dropna()
    bank_text.append(incomes)
    #print(bank_text, "YeY")
    #print("\n")
    
    #logo(filename)
    #print(f"Total Debit:%.2f \nTotal Credit:%.2f \nTotal Balance:%.2f" % (t_debit, t_credit, t_bal) )
    json_result = {
        "Account Number" : bank_text[0],
        "Account Name" : bank_text[1],
        "IFSC Code": bank_text[2],
        "Opening Balance": bank_text[3],
        "Closing Balance": bank_text[4],
        "Total Debit Summary": bank_text[5],
        "Total Credit Summary": bank_text[6],
        "Total Balance Summary": bank_text[7],

        #"Expenses": bank_text[8],
        #"Incomes": bank_text[9]
    }
    return json_result
 
#bank_details("text2.pdf")
def logo(filename):

    doc = fitz.open(filename)
    for i in range(len(doc)):
        for img in doc.getPageImageList(i):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n < 5:       # this is GRAY or RGB
                pix.writePNG("./media/p%s-%s.png" % (i, xref))
            else:               # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                pix1.writePNG("./media/p%s-%s.png" % (i, xref))
                pix1 = None
            pix = None


