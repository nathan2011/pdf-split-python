import PyPDF2
import requests
from io import BytesIO

pdf_links = ["https://altdrxlive.s3.amazonaws.com/9439/BPLIO.04/9439-1731653804-TradeXAgreement.pdf","https://altdrxlive.s3.amazonaws.com/9127/BPLIO.04/9127-1731646491-TradeXAgreement.pdf","https://altdrxlive.s3.amazonaws.com/3750/BPLIO.04/3750-1725451953-TradeXAgreement.pdf"]
# pdf_links = ["1.pdf", "2.pdf", "3.pdf"]
# Initialize a PDF merger object
pdf_merger = PyPDF2.PdfMerger()

# Iterate over the PDF links and download each PDF
for link in pdf_links:
    try:
        response = requests.get(link)
        if response.status_code == 200:
            pdf_bytes = BytesIO(response.content)
            pdf_merger.append(pdf_bytes)
        else:
            print(f"Failed to download PDF from {link}")
    except Exception as e:
        print(f"Error: {str(e)}")

# Specify the output file name
output_filename = "framework_agreement_bplio_release_b.pdf"

# Write the merged PDF to a file
with open(output_filename, "wb") as output_file:
    pdf_merger.write(output_file)

# Close the PDF merger object
pdf_merger.close()

print(f"Merged PDF saved as {output_filename}")