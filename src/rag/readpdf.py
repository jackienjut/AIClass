from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer


def extract_text_from_pdf(file_name, page_numbers=None, min_line_length=1):
    '''从pdf中指定的页码中提取文本'''
    paragraphs = []
    buffer = ''
    full_text = ''

    for i, page_layout in enumerate(extract_pages(file_name)):
        if page_numbers is not None and i not in page_numbers:
            continue
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                if element.get_text().strip() == '':
                    continue
                if element.get_text().strip() == '\n':
                    continue
                if element.get_text().strip() == '\r':
                    continue
                else:
                    full_text += element.get_text()

    '''按照空行分割，将文本重新组织成段落'''

    for line in full_text.split('\n'):
        if line == '':
            paragraphs.append(buffer)
            buffer = ''
        else:
            buffer += line + '\n'
            if line.strip() == '':
                paragraphs.append(buffer)
                buffer = ''
    if buffer != '':
        paragraphs.append(buffer)
    return paragraphs


if __name__ == '__main__':
    paragraphs = extract_text_from_pdf('llama2.pdf', min_line_length=10)
    for para in paragraphs[:4]:
        print(para + "\n")
