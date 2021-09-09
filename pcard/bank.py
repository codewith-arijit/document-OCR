import tabula
import pandas as pd

from PyPDF2 import PdfFileReader
import re
import pdftotext


def bank_details(filename):
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
    acc_name= "Account Name: " + '\n'.join([re.sub(r'Account Name\s+:', '', line) for line in data.splitlines() if 'Account Name' in line])
    acc_no= "Account Number: "+ '\n'.join([re.sub(r'Account Number\s+:', '', line) for line in data.splitlines() if 'Account Number' in line])
    acc_code = "IFS Code: "+ '\n'.join([re.sub(r'IFS Code\s+:', '', line) for line in data.splitlines() if 'IFS Code' in line])
    
    op_bal = "Opening Balance: " + str(bal[0])
    cl_bal = "Closing Balance: " + str(bal[(len(bal)-1)])
    t_debit = "Total Debit Summary: " + str(t_debit)
    t_credit = "Total Credit Summary: " + str(t_credit)
    t_bal = "Total Balance Summary: " + str(t_bal)
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
    

    #print(f"Total Debit:%.2f \nTotal Credit:%.2f \nTotal Balance:%.2f" % (t_debit, t_credit, t_bal) )
    return bank_text

#bank_details("text2.pdf")