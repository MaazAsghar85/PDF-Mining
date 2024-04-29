import fitz  # PyMuPDF

def extract_content_by_font_size_and_style(pdf_path):
    content = []
    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        print("\n\n\n\nPage: ", page)
        blocks = page.get_text("dict")["blocks"]
        print("\n\n\n\n\n\nBlocks: ", blocks)

if __name__ == "__main__":
    pdf_path = 'data_2336.pdf'
    extract_content_by_font_size_and_style(pdf_path)