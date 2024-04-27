import fitz  # PyMuPDF

def extract_content_by_font_size_and_style(pdf_path):
    content = []
    doc = fitz.open(pdf_path)
    
    def is_bold(font_name):
        # Checks for common bold indicators in font names
        bold_indicators = ["Bold", "CMBX9", "NimbusRomNo9L-Medi"]
        return any(bold in font_name for bold in bold_indicators)

    # To store font size frequency
    font_size_frequency = {}

    # Variables to track the current segment
    current_text = ""
    current_font_size = None
    current_style = None

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]
        
        for b in blocks:
            if 'lines' in b:
                for l in b["lines"]:
                    for s in l["spans"]:
                        text = s["text"]
                        font_size = s["size"]
                        font_name = s["font"]
                        bold = is_bold(font_name)
                        style = "Bold" if bold else "Regular"

                        # Check if the current span continues the current segment
                        if font_size == current_font_size and style == current_style:
                            current_text += " " + text
                        else:
                            # If there's a current segment, append it to content and reset
                            if current_text:
                                content.append((current_text, current_font_size, current_style))
                                if current_font_size in font_size_frequency:
                                    font_size_frequency[current_font_size] += 1
                                else:
                                    font_size_frequency[current_font_size] = 1
                            # Start a new segment
                            current_text = text
                            current_font_size = font_size
                            current_style = style

    # Append the last segment if it exists
    if current_text:
        content.append((current_text, current_font_size, current_style))
        if current_font_size in font_size_frequency:
            font_size_frequency[current_font_size] += 1
        else:
            font_size_frequency[current_font_size] = 1

    # Find the most common font size
    most_common_font_size = max(font_size_frequency, key=font_size_frequency.get)

    class MyDictionary:
        def __init__(self):
            self.items = {}

        def add(self, key, value):
            self.items[key] = value

        def remove(self, key):
            if key in self.items:
                del self.items[key]
            else:
                print("Key not found.")

        def get(self, key):
            if key in self.items:
                return self.items[key]
            else:
                return None

        def keys(self):
            return list(self.items.keys())

        def values(self):
            return list(self.items.values())

        def __str__(self):
            return str(self.items)
        
    my_dict = MyDictionary()

    found = False
    for text, font_size, style in content:
        if text == 'Service' or text == 'Target':
            myText = text
            found = True
            continue
        if found:
            my_dict.add(myText, text)
            found = False

    print("\nService: ", my_dict.get("Service"))
    print("\nTarget: ", my_dict.get("Target"))

if __name__ == "__main__":
    pdf_path = r'.\data_2336.pdf'
    extract_content_by_font_size_and_style(pdf_path)