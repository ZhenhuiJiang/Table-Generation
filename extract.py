"""
extract the location of some characters in pdf.
"""



import pdf
from pdfminer.layout import LTTextBoxHorizontal, LTAnno
import os
import matplotlib.image as mpimg

img=mpimg.imread('./train_image/no_qianzhui_a_0.png')
height,width,channel=img.shape
file_path_list = []


def load_pdf(file_path=None):
    if file_path:
        doc = pdf.load_pdf_as_doc(file_path)
        return pdf.parse_pdf_as_dict(doc)
    else:
        pdf_dict_list = []
        for _file_path in file_path_list:
            doc = pdf.load_pdf_as_doc(_file_path)
            pdf_dict_list.append(pdf.parse_pdf_as_dict(doc))
        return pdf_dict_list


def get_data_not_table(file_path, file_name):


    file_name = '.'.join([file_name.split('.pdf')[0], 'txt'])
    pdf_dict = load_pdf(file_path)
    data_list_whole = {}
    for page_number, page_object in pdf_dict.items():
        data_list = []

        layout, [pdf_width, pdf_height] = page_object[0], page_object[1]
        w_rate = float(width / pdf_width)
        h_rate = float(height / pdf_height)

        for element in layout:
            if isinstance(element, LTTextBoxHorizontal):
                for text_area in element:
                    # print(text_area)
                    for char_area in text_area:
                        if not isinstance(char_area, LTAnno):
                            # print(char_area)
                            x1, y1, x2, y2 = char_area.bbox
                            if char_area.get_text() == '#':
                                # x1, y1, x2, y2 = element.bbox
                                data_list.append({
                                    'location': [int(x1 * w_rate -20 + 250),#+250 is padding
                                                 int((pdf_height - y1) * h_rate - 60)],
                                    'value': char_area.get_text()
                                })
                            if char_area.get_text() == '%':
                # x1, y1, x2, y2 = element.bbox
                                data_list.append({
                                    'location': [int(x1*w_rate - 20 + 250),
                                                 int((pdf_height-y1)*h_rate-30)],
                                    'value': char_area.get_text()
                                })
                            if char_area.get_text() == '$':
                                data_list.append({
                                    'location': [int(x1*w_rate+20+250),
                                                 int((pdf_height-y1)*h_rate)],
                                    'value': char_area.get_text()
                                })
        data_list_whole[page_number] = data_list
    with open('./not_table_{}'.format(file_name), 'w') as f:
        f.writelines(str(data_list_whole))



def get_data_table(file_path, file_name):


    file_name = '.'.join([file_name.split('.pdf')[0], 'txt'])
    pdf_dict = load_pdf(file_path)
    data_list_whole = {}
    for page_number, page_object in pdf_dict.items():
        data_list = []

        layout, [pdf_width, pdf_height] = page_object[0], page_object[1]
        w_rate = float(width / pdf_width)
        h_rate = float(height / pdf_height)

        for element in layout:
            if isinstance(element, LTTextBoxHorizontal):
                for text_area in element:
                    # print(text_area)
                    for char_area in text_area:
                        if not isinstance(char_area, LTAnno):
                            # print(char_area)
                            x1, y1, x2, y2 = char_area.bbox
                            if char_area.get_text() == '@':
                # x1, y1, x2, y2 = element.bbox
                                data_list.append({
                                    'location': [int(x1*w_rate-20+250),#+250 is padding
                                                 int((pdf_height-y1)*h_rate-30)],
                                    'value': char_area.get_text()
                                })
                            if char_area.get_text() == '*':
                                data_list.append({
                                    'location': [int(x1*w_rate+20+250),
                                                 int((pdf_height-y1)*h_rate)],
                                    'value': char_area.get_text()
                                })
        data_list_whole[page_number] = data_list
    with open('./table_{}'.format(file_name), 'w') as f:
        f.writelines(str(data_list_whole))



for _, dirs, files in os.walk('./'):
    for file in files:
        if file.endswith('.pdf') and file.startswith(('qianzhui')):
            get_data_not_table('./{}'.format(file), file)
            get_data_table('./{}'.format(file), file)