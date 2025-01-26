import pdfplumber
import pandas as pd
from openpyxl import Workbook

def extract_bank_statement(pdf_path):
    data = []
    
    # Open and read the PDF
    with pdfplumber.open("OpTransactionHistory26-01-2025.pdf") as pdf:
        for page in pdf.pages:
            # Extract table data
            tables = page.extract_tables()
            
            # Process each table on the page
            for table in tables:
                for row in table[1:]:  # Skip the header row
                    try:
                        transaction_date = row[2]  # "Transaction Date" column
                        withdrawal_amount = row[5]  # "Withdrawal Amount (INR)" column
                        
                        # Only process rows with valid withdrawal amounts
                        if withdrawal_amount and float(withdrawal_amount) > 0:
                            data.append({
                                "Transaction Date": transaction_date,
                                "Debit": float(withdrawal_amount)
                            })
                    except (ValueError, IndexError):
                        # Skip invalid rows
                        continue
    
    return data

def process_debits(data):
    # Convert to DataFrame
    df = pd.DataFrame(data)
    df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], dayfirst=True)
    
    # Group by date and sum debit amounts
    summary = df.groupby('Transaction Date')['Debit'].sum().reset_index()
    return summary

def save_to_excel(df, output_path):
    # Save the DataFrame to an Excel file
    df.to_excel(output_path, index=False, engine='openpyxl')
    print(f"Excel file saved to: {output_path}")

# Main script
pdf_path = "bank_statement.pdf"  # Replace with your PDF file path
output_path = "debit_summary.xlsx"

# Step 1: Extract data from the PDF
data = extract_bank_statement(pdf_path)

# Step 2: Process data to calculate total debit amounts date-wise
summary = process_debits(data)

# Step 3: Save the summary to an Excel file
save_to_excel(summary, output_path)
