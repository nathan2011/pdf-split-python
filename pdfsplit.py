import requests
from PyPDF2 import PdfReader, PdfWriter

# Function to download the PDF from the URL
def download_pdf(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded PDF: {filename}")
        return filename
    else:
        raise Exception(f"Failed to download PDF from {url}. Status code: {response.status_code}")

# Function to split the PDF into three parts
def split_pdf(input_pdf, output_pdf_prefix):
    reader = PdfReader(input_pdf)
    total_pages = len(reader.pages)
    page_ranges = [
        (0, 21),   # Pages 1 to 20
        (21, 24),  # Pages 21 to 22
        (24, 56)   # Pages 23 to 24
    ]
    
    for i, (start, end) in enumerate(page_ranges, start=1):
        writer = PdfWriter()
        for page_num in range(start, min(end, total_pages)):  # Avoid index out of range
            writer.add_page(reader.pages[page_num])
        output_pdf = f"{output_pdf_prefix}_Part{i}.pdf"
        with open(output_pdf, 'wb') as f:
            writer.write(f)
        print(f"Created: {output_pdf}")

# Main script
if __name__ == "__main__":
    # Array of tuples containing AWS S3 links and investor IDs
    pdf_links_with_ids = [
        # ("https://altdrxlive.s3.amazonaws.com/3956/BPLIO.02/3956-1711731435-EoisubscriptionAgreement.pdf","3956"),
        ("https://altdrxlive.s3.amazonaws.com/3875/BPLIO.02/3875-1711949119-EoisubscriptionAgreement.pdf","3875"),
        ("https://altdrxlive.s3.amazonaws.com/4240/BPLIO.02/4240-1712041216-EoisubscriptionAgreement.pdf","4240"),
        ("https://altdrxlive.s3.amazonaws.com/4273/BPLIO.02/4273-1711854222-EoisubscriptionAgreement.pdf","4273"),
        ("https://altdrxlive.s3.amazonaws.com/4421/BPLIO.02/4421-1711907400-EoisubscriptionAgreement.pdf","4421"),
        ("https://altdrxlive.s3.amazonaws.com/4467/BPLIO.02/4467-1711723174-EoisubscriptionAgreement.pdf","4467"),
        ("https://altdrxlive.s3.amazonaws.com/4705/BPLIO.02/4705-1711723174-EoisubscriptionAgreement.pdf","4705"),
        ("https://altdrxlive.s3.amazonaws.com/4765/BPLIO.02/4765-1712414259-EoisubscriptionAgreement.pdf","4765"),
        # Add more (URL, investor ID) pairs as needed
    ]
    
    for idx, (link, investor_id) in enumerate(pdf_links_with_ids, start=1):
        try:
            # Generate filenames using the investor ID
            input_pdf = f"{investor_id}.pdf"
            output_prefix = investor_id
            
            # Step 1: Download the PDF
            download_pdf(link, input_pdf)
            
            # Step 2: Split the PDF into three parts
            split_pdf(input_pdf, output_prefix)
        
        except Exception as e:
            print(f"Error processing link {idx}: {link}. Error: {e}")
