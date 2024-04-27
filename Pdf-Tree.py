import fitz  # PyMuPDF

fonts_list = []

class Node:
    def __init__(self, text, font_size, style):
        self.text = text
        self.font_size = font_size
        self.style = style
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, text, font_size, style):
        if not self.head:
            self.head = Node(text, font_size, style)
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = Node(text, font_size, style)

    def display(self):
        print()
        current_node = self.head
        while current_node:
            count = 0
            for f in fonts_list:
                if f == current_node.font_size:
                    break
                else:
                    count += 1
            print('    ' * count, end='')
            print(current_node.text)
            current_node = current_node.next

def extract_content_by_font_size_and_style(pdf_path):
    List = LinkedList()
    content = []
    doc = fitz.open(pdf_path)
    
    def is_bold(font_name):
        bold_indicators = ["Bold", "CMBX9", "NimbusRomNo9L-Medi"]
        return any(bold in font_name for bold in bold_indicators)
    
    font_size_frequency = {}

    current_text = ""
    current_font_size = None
    current_style = None

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]
        
        for b in blocks:
            for l in b["lines"]:
                for s in l["spans"]:
                    text = s["text"]
                    font_size = s["size"]
                    font_name = s["font"]
                    bold = is_bold(font_name)
                    style = "Bold" if bold else "Regular"

                    if font_size == current_font_size and style == current_style:
                        current_text += " " + text
                    else:
                        if current_text:
                            content.append((current_text, current_font_size, current_style))
                            if current_font_size in font_size_frequency:
                                font_size_frequency[current_font_size] += 1
                            else:
                                font_size_frequency[current_font_size] = 1

                        current_text = text
                        current_font_size = font_size
                        current_style = style

    if current_text:
        content.append((current_text, current_font_size, current_style))
        if current_font_size in font_size_frequency:
            font_size_frequency[current_font_size] += 1
        else:
            font_size_frequency[current_font_size] = 1

    most_common_font_size = max(font_size_frequency, key=font_size_frequency.get)

    for text, font_size, style in content:
        if font_size != most_common_font_size or (font_size == most_common_font_size and style == "Bold"):
            if font_size not in fonts_list:
                fonts_list.append(font_size)
                fonts_list.sort(reverse = True)
            List.append(text, font_size, style)

    List.display()

if __name__ == "__main__":
    pdf_path = r'.\my2.pdf'
    extract_content_by_font_size_and_style(pdf_path)