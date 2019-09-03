from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.layout import LAParams
from pdfminer.layout import LTTextBoxHorizontal
from pdfminer.layout import LTRect
from pdfminer.layout import LTFigure
from pdfminer.layout import LTAnno
from pdfminer.layout import LTLine

from PIL import Image

import pdf

import cv2
import numpy as np
import pdf2image
import random


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


def show_search_line(file_path, threshold):
    fp = open(file_path, 'rb')
    images = pdf2image.convert_from_bytes(fp.read(), dpi=300)

    pdf_dict = load_pdf(file_path)

    img = images[0]
    img_w, img_h = img.size

    page_object = pdf_dict[0]

    layout, [pdf_width, pdf_height] = page_object[0], page_object[1]
    w_rate = float(img_w / pdf_width)
    h_rate = float(img_h / pdf_height)
    img = np.array(img)

    cv2.line(img,
             (0, int(threshold * img_h)),
             (int(img_w), int(threshold * img_h)),
             color=(255, 0, 0),
             thickness=3)
    result = Image.fromarray(img)
    result.show()


def show_search_line_manual(file_path, page_number, thresholds):
    fp = open(file_path, 'rb')
    images = pdf2image.convert_from_bytes(fp.read(), dpi=300)

    pdf_dict = load_pdf(file_path)

    img = images[page_number]
    img_w, img_h = img.size

    page_object = pdf_dict[page_number]

    layout, [pdf_width, pdf_height] = page_object[0], page_object[1]
    w_rate = float(img_w / pdf_width)
    h_rate = float(img_h / pdf_height)
    img = np.array(img)

    for threshold in thresholds:
        cv2.line(img,
                 (0, int(threshold * img_h)),
                 (int(img_w), int(threshold * img_h)),
                 color=(255, 0, 0),
                 thickness=3)
    result = Image.fromarray(img)
    result.show()


def show_characters_and_rect_area(file_path):
    fp = open(file_path, 'rb')
    images = pdf2image.convert_from_bytes(fp.read(), dpi=300)

    pdf_dict = load_pdf(file_path)
    for page_number, page_object in pdf_dict.items():
        img = images[page_number]
        img_w, img_h = img.size

        layout, [pdf_width, pdf_height] = page_object[0], page_object[1]
        w_rate = float(img_w / pdf_width)
        h_rate = float(img_h / pdf_height)
        img = np.array(img)

        for element in layout:
            if isinstance(element, LTRect):
                # print(element)
                x1, y1, x2, y2 = element.bbox
                # cv2.rectangle(img,
                #               (int(x1 * w_rate),
                #                int((pdf_height - y1) * h_rate)),
                #               (int(x2 * w_rate),
                #                int((pdf_height - y2) * h_rate)),
                #               (0, 255, 0),
                #               thickness=5)
                # cv2.circle(img,
                #            (int(x1 * w_rate),
                #             int((pdf_height - y1) * h_rate)),
                #            5,
                #            (255, 0, 0),
                #            thickness=5)
                # cv2.circle(img,
                #            (int(x2 * w_rate),
                #             int((pdf_height - y2) * h_rate)),
                #            5,
                #            (255, 0, 0),
                #            thickness=5)
            elif isinstance(element, LTTextBoxHorizontal):
                print(element.get_text())
                x1, y1, x2, y2 = element.bbox
                cv2.rectangle(img,
                              (int(x1 * w_rate),
                               int((pdf_height - y1) * h_rate)),
                              (int(x2 * w_rate),
                               int((pdf_height - y2) * h_rate)),
                              (255, 0, 0),
                              thickness=1)
                """
                for text_area in element:
                    # print(text_area)
                    for char_area in text_area:
                        if not isinstance(char_area, LTAnno):
                            # print(char_area)
                            x1, y1, x2, y2 = char_area.bbox
                            cv2.rectangle(img,
                                          (int(x1 * w_rate),
                                           int((pdf_height - y1) * h_rate)),
                                          (int(x2 * w_rate),
                                           int((pdf_height - y2) * h_rate)),
                                          (255, 0, 0),
                                          thickness=1)
                """
                # print('-----------------')

        # img = cv2.resize(img, (int(img_w / 2), int(img_h / 2)))

        result = Image.fromarray(img)
        result.show()


def show_characters(file_path, coordinate_list, _page_number):
    fp = open(file_path, 'rb')
    images = pdf2image.convert_from_bytes(fp.read(), dpi=300)

    pdf_dict = load_pdf(file_path)
    for page_number, page_object in pdf_dict.items():
        if page_number != _page_number:
            continue
        img = images[page_number]
        img_w, img_h = img.size

        layout, [pdf_width, pdf_height] = page_object[0], page_object[1]
        w_rate = float(img_w / pdf_width)
        h_rate = float(img_h / pdf_height)
        img = np.array(img)

        for coordinate in coordinate_list:
            x1, y1, x2, y2, _ = coordinate
            cv2.rectangle(img,
                          (int(x1 * w_rate),
                           int((pdf_height - y1) * h_rate)),
                          (int(x2 * w_rate),
                           int((pdf_height - y2) * h_rate)),
                          (random.randint(0, 255),
                           random.randint(0, 255),
                           random.randint(0, 255)),
                          thickness=3)

        result = Image.fromarray(img)
        result.show()


def show_rect(file_path, coordinate_list, _page_number):
    fp = open(file_path, 'rb')
    images = pdf2image.convert_from_bytes(fp.read(), dpi=300)

    pdf_dict = load_pdf(file_path)
    for page_number, page_object in pdf_dict.items():
        if page_number != _page_number:
            continue
        img = images[page_number]
        img_w, img_h = img.size

        layout, [pdf_width, pdf_height] = page_object[0], page_object[1]
        w_rate = float(img_w / pdf_width)
        h_rate = float(img_h / pdf_height)
        img = np.array(img)

        for coordinate in coordinate_list:
            x1, y1, x2, y2 = coordinate
            cv2.rectangle(img,
                          (int(x1 * w_rate),
                           int((pdf_height - y1) * h_rate)),
                          (int(x2 * w_rate),
                           int((pdf_height - y2) * h_rate)),
                          (random.randint(0, 255),
                           random.randint(0, 255),
                           random.randint(0, 255)),
                          thickness=2)

        result = Image.fromarray(img)
        result.show()


def show_both(file_path, char_result, rect_result, _page_number):
    fp = open(file_path, 'rb')
    images = pdf2image.convert_from_bytes(fp.read(), dpi=300)

    pdf_dict = load_pdf(file_path)
    for page_number, page_object in pdf_dict.items():
        if page_number != _page_number:
            continue
        img = images[page_number]
        img_w, img_h = img.size

        layout, [pdf_width, pdf_height] = page_object[0], page_object[1]
        w_rate = float(img_w / pdf_width)
        h_rate = float(img_h / pdf_height)
        img = np.array(img)

        for coordinate in rect_result:
            x1, y1, x2, y2 = coordinate
            cv2.rectangle(img,
                          (int(x1 * w_rate),
                           int((pdf_height - y1) * h_rate)),
                          (int(x2 * w_rate),
                           int((pdf_height - y2) * h_rate)),
                          (random.randint(0, 255),
                           random.randint(0, 255),
                           random.randint(0, 255)),
                          thickness=3)

        for coordinate in char_result:
            x1, y1, x2, y2, _ = coordinate
            cv2.rectangle(img,
                          (int(x1 * w_rate),
                           int((pdf_height - y1) * h_rate)),
                          (int(x2 * w_rate),
                           int((pdf_height - y2) * h_rate)),
                          (random.randint(0, 255),
                           random.randint(0, 255),
                           random.randint(0, 255)),
                          thickness=3)
            # cv2.circle(img,
            #            (int(abs(x1 + x2) / 2 * w_rate),
            #             int((pdf_height - abs(y1 + y2) / 2) * h_rate)),
            #            5, (0, 0, 0), thickness=7)

        result = Image.fromarray(img)
        result.show()


def show_everything(file_path, _page_number):
    fp = open(file_path, 'rb')
    images = pdf2image.convert_from_bytes(fp.read(), dpi=300)

    pdf_dict = load_pdf(file_path)
    for page_number, page_object in pdf_dict.items():
        if page_number != _page_number:
            continue
        img = images[page_number]
        img_w, img_h = img.size
        layout, [pdf_width, pdf_height] = page_object[0], page_object[1]
        # print(pdf_width, pdf_height)
        w_rate = float(img_w / pdf_width)
        h_rate = float(img_h / pdf_height)
        img = np.array(img)

        for element in layout:
            # print(element)
            if isinstance(element, LTRect):
                x1, y1, x2, y2 = element.bbox
                cv2.rectangle(img,
                              (int(x1 * w_rate),
                               int((pdf_height - y1) * h_rate)),
                              (int(x2 * w_rate),
                               int((pdf_height - y2) * h_rate)),
                              (255, 0, 0),
                              thickness=2)

            elif isinstance(element, LTTextBoxHorizontal):
                # x1, y1, x2, y2 = element.bbox
                # cv2.rectangle(img,
                #               (int(x1 * w_rate),
                #                int((pdf_height - y1) * h_rate)),
                #               (int(x2 * w_rate),
                #                int((pdf_height - y2) * h_rate)),
                #               (0, 255, 0),
                #               thickness=2)
                for text_area in element:
                    print(text_area)
                    for char_area in text_area:
                        if not isinstance(char_area, LTAnno):
                            # print(char_area)
                            x1, y1, x2, y2 = char_area.bbox
                            cv2.rectangle(img,
                                          (int(x1 * w_rate),
                                           int((pdf_height - y1) * h_rate)),
                                          (int(x2 * w_rate),
                                           int((pdf_height - y2) * h_rate)),
                                          (0, 255, 0),
                                          thickness=2)

            elif isinstance(element, LTFigure):
                print(element)
                x1, y1, x2, y2 = element.bbox
                cv2.rectangle(img,
                              (int(x1 * w_rate),
                               int((pdf_height - y1) * h_rate)),
                              (int(x2 * w_rate),
                               int((pdf_height - y2) * h_rate)),
                              (255, 0, 255),
                              thickness=2)

            # elif isinstance(element, LTLine):
            #     x1, y1, x2, y2 = element.bbox
            #     cv2.line(img,
            #              (int(x1 * w_rate),
            #               int((pdf_height - y1) * h_rate)),
            #              (int(x2 * w_rate),
            #               int((pdf_height - y2) * h_rate)),
            #              (0, 255, 0),
            #              thickness=5)
        result = Image.fromarray(img)
        result.show()
        break


if __name__ == '__main__':
    # show_characters_and_rect_area('./data/142312-Customer-Test.pdf')
    # show_search_line_manual(file_path_list[5],
    #                         0,
    #                         [0.25, 0.89])

    file_path_list = ['../files/易到行程单.pdf',
                      '../files/滴滴出行行程报销单-6-多页.pdf',
                      '../files/神州专车电子行程单.pdf',
                      '../files/美团打车行程单.pdf',
                      '../files/首约行程单.pdf',
                      '../files/曹操专车电子行程单-3-多页.pdf']

    # for file_path in file_path_list:
    #     print(file_path)
    #     show_everything(file_path)
    #     print('------------')
    show_everything('without_line.pdf', _page_number=0)
    # show_rect('../files/3.pdf',
    #           [[50, 740, 140.4, 764.5]], 0)
