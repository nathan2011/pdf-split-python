import PyPDF2

# Open the PDF files you want to merge
pdf1 = open("1.pdf", "rb")
pdf2 = open("2.pdf", "rb")
pdf3 = open("3.pdf", "rb")
# pdf4 = open("BPLIO4.pdf", "rb")


# Create PdfFileMerger object
pdf_merger = PyPDF2.PdfMerger()

# Append the PDF files to the merger object
pdf_merger.append(pdf1)
pdf_merger.append(pdf2)
pdf_merger.append(pdf3)
# pdf_merger.append(pdf4)

# pdf_merger.append(pdf3)
# pdf_merger.append(pdf4)
# pdf_merger.append(pdf3)
# pdf_merger.append(pdf4)
# pdf_merger.append(pdf5)

# Create a new PDF file to write the merged content
output_pdf = open("BPLIO RELEASE B Framework.pdf", "wb")

# Write the merged content to the new PDF file
pdf_merger.write(output_pdf)

# Close all files
pdf1.close()
pdf2.close()
pdf3.close()
# pdf4.close()
# pdf3.close()
# pdf4.close()
# pdf5.close()
output_pdf.close()

print("PDFs merged successfully into 'framework.pdf'")