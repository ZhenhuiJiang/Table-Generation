from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfdocument import PDFDocument
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.layout import LAParams
from pdfminer.layout import LTTextBoxHorizontal
from pdfminer.layout import LTRect
from pdfminer.layout import LTAnno
from pdfminer.layout import LTFigure

import codecs
import json
import re


def load_pdf_as_doc(pdf_file_path):
    """
    parse pdf and return origin object
    :param pdf_file_path: pdf file path
    :return: origin object
    """
    try:
        fp = open(pdf_file_path, 'rb')
    except Exception as e:
        return e

    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    return doc


def parse_pdf_as_dict(doc):
    """
    parse pdf as dict
    parse object and return a dict
    pdf_dict = {
        1: [page_1_layout, [page_1_width, page_1_height]],
        2: [page_2_layout, [page_2_width, page_2_height]],
        ...
        }
    :param doc: pdf origin object
    :return: pdf_dict
    """
    pdf_dict = {}

    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for (page_number, page) in enumerate(PDFPage.create_pages(doc)):
        pdf_width = page.mediabox[2]
        pdf_height = page.mediabox[3]
        interpreter.process_page(page)
        layout = device.get_result()
        pdf_dict[page_number] = [layout, [pdf_width, pdf_height]]
    return pdf_dict


def identify_company(pdf_dict):
    """
    identify company (six companies now)
    using regular expression & coordinate threshold <- see detail in config
    :param pdf_dict: pdf dict
    :return: None if no match
             [company, company_chinese_name] if match
    """
    with codecs.open('../config/ei_identify_company.json', 'r', 'utf-8') as f:
        config = json.load(f)

    first_page_object = pdf_dict[0]

    layout = first_page_object[0]
    _, pdf_height = first_page_object[1]

    for company, search_rule in config.items():
        company_chinese_name = search_rule['type']
        search_keyword = search_rule['keyword']
        searching_threshold = search_rule['searching_threshold']
        y_coordinate_threshold = pdf_height * (1 - searching_threshold)

        for element in layout:
            if isinstance(element, LTTextBoxHorizontal):
                x1, y1, x2, y2 = element.bbox
                if y1 > y_coordinate_threshold:
                    re_result = re.search(search_keyword, element.get_text())
                    if re_result is not None:
                        return company, company_chinese_name

    return None


def fetch_pdf_page_info_dict(pdf_dict):
    """
    fetch pdf page info
    include (text_area, rect_area, figure, line, ...)
    :param pdf_dict: pdf dict
    :return: pdf_page_info_dict =
        {
            0: [
                [pdf_width, pdf_height],
                text_area_list,
                rect_area_list,
                {
                    'figure': [[x1, y1, x2, y2], [], ...]
                    'line': [[x1, y1, x2, y2], [], ...]
                    ...
                }
            ],
            1: [...]
            ...
        }
    """
    pdf_page_info_dict = {}
    for page_number, page_object in pdf_dict.items():
        layout = page_object[0]
        text_areas, rect_areas, other_areas = _fetch_all_pdf_info(layout)
        pdf_page_info_dict[page_number] = [
            page_object[1],
            text_areas,
            rect_areas,
            other_areas
        ]

    return pdf_page_info_dict


def _fetch_all_pdf_info(pdf_layout):
    """
    main workflow of fetching pdf info

    :param pdf_layout:
    :return:
    """
    char_list = []
    rect_list = []
    others_dict = {}
    for element in pdf_layout:
        if isinstance(element, LTTextBoxHorizontal):
            char_list = _fetch_single_element_char_list(element, char_list)
        elif isinstance(element, LTRect):
            rect_list = _fetch_single_element_rect_list(element, rect_list)
        else:
            others_dict = _fetch_single_element_required_info_as_dict(
                element=element,
                others_dict=others_dict
            )

    char_list = _merge_characters(char_list)

    return char_list, rect_list, others_dict


def _fetch_single_element_char_list(element, char_list):
    for text_area in element:
        for char_area in text_area:
            if isinstance(char_area, LTAnno):
                continue
            x1, y1, x2, y2 = char_area.bbox

            char_object = [round(x1, 3),
                           round(y1, 3),
                           round(x2, 3),
                           round(y2, 3),
                           char_area.get_text()]

            # remove duplicate
            if char_object in char_list:
                pass
            else:
                char_list.append(char_object)

    return char_list


def _fetch_single_element_rect_list(element, rect_list):
    x1, y1, x2, y2 = element.bbox

    rect_object = [
        round(x1, 3),
        round(y1, 3),
        round(x2, 3),
        round(y2, 3)
    ]

    if rect_object in rect_list:
        pass
    else:
        rect_list.append(rect_object)

    return rect_list


def _fetch_single_element_required_info_as_dict(element, others_dict):
    if isinstance(element, LTFigure):
        x1, y1, x2, y2 = element.bbox

        figure_object = [
            round(x1, 3),
            round(y1, 3),
            round(x2, 3),
            round(y2, 3)
        ]

        if 'figure' not in others_dict.keys():
            others_dict['figure'] = []

        if figure_object in others_dict['figure']:
            pass
        else:
            others_dict['figure'].append(figure_object)

    return others_dict


def _merge_characters(char_list):
    """
    merge sorted characters

    1. choose one char
    2. for loop:
        -> find a char which left/right/top/bottom equals
           or in the interval of thresholds
        -> enlarge char bounding box
        -> end when satisfied end condition
        -> add in merged_text_area_list

    :param char_list: char list
    :return: merged_text_area_list: merged_text_area_list =
        [
            [x1, y1, x2, y2, text],
            [x1, y1, x2, y2, text],
            ...
        ]
    """
    merged_text_area_list = []

    previous_x_1, previous_y_1 = None, None
    previous_x_2, previous_y_2 = None, None
    temp_characters = []

    is_end_flag = True
    while len(char_list) > 0:
        if is_end_flag:
            is_end_flag = False
            previous_x_1 = char_list[0][0]
            previous_y_1 = char_list[0][1]
            previous_x_2 = char_list[0][2]
            previous_y_2 = char_list[0][3]
            temp_characters.append(char_list[0][4])
            char_list.pop(0)
        else:
            for char in char_list:
                current_x_1 = char[0]
                current_x_2 = char[2]
                current_y_2 = char[3]
                current_char = char[4]
                if abs(previous_x_2 - current_x_1) < 1 \
                        and abs(previous_y_2 - current_y_2) < 5:
                    previous_x_2 = current_x_2
                    temp_characters.append(current_char)
                    char_list.remove(char)
                    is_end_flag = False
                    break
                elif abs(previous_x_1 - current_x_2) < 1 \
                        and abs(previous_y_2 - current_y_2) < 5:
                    previous_x_1 = current_x_1
                    temp_characters.insert(0, current_char)
                    char_list.remove(char)
                    is_end_flag = False
                    break
                else:
                    is_end_flag = True

            if is_end_flag:
                merged_text_area_list.append([
                    previous_x_1,
                    previous_y_1,
                    previous_x_2,
                    previous_y_2,
                    temp_characters
                ])
                temp_characters = []

    if len(temp_characters) != 0:
        merged_text_area_list.append([
            previous_x_1,
            previous_y_1,
            previous_x_2,
            previous_y_2,
            temp_characters
        ])

    for merged_text_area in merged_text_area_list:
        merged_text_area[4] = ''.join(merged_text_area[4])
        # merged_text_area[4] = ''.join(merged_text_area[4].split())

    return merged_text_area_list


def extract_regular_table_as_list(text_area_list,
                                  rect_area_list,
                                  is_regular_table_type,
                                  searching_threshold):
    """
    analyze text_area_list and rect_area_list
    and create a two dimension list type result

    if regular type:
        -> use all different x1 & x2 coordinates as x lines
        -> use all different y1 & y2 coordinates as y lines

    if irregular type:
        -> use all different x1 & x2 coordinates as x lines
        -> use all different y1 & y2 & bottom line as y lines

    create two dimension list size of len(x_line) * len(y_line)

    for each text area:
        -> if center point in cell area:
            -> add into cell

    extract text in each cell area:
        -> if multiple text areas:
            -> merge ordered by y coordinate
        -> if empty:
            -> add text as ''

    if whole row's text are '':
        -> remove

    :param text_area_list: text area list
    :param rect_area_list: rect area list
    :param is_regular_table_type: True or False (caocao meituan)
    :param searching_threshold: list = [coordinate, coordinate/string]
    :return:
    """
    top_line = round(searching_threshold[0], 3)
    _bottom_line = searching_threshold[1]
    # default bottom line is 0 (the bottom in one pdf page)
    bottom_line = 0

    # if re type bottom line, find through regular expression
    if type(_bottom_line) is str:
        for text_area in text_area_list:
            x1, y1, x2, y2, text = text_area
            re_result = re.search(_bottom_line, text)
            if re_result:
                bottom_line = y2
                break
    else:
        bottom_line = _bottom_line

    bottom_line = round(bottom_line, 3)

    satisfied_rect_area_list = []

    for rect_area in rect_area_list:
        x1, y1, x2, y2 = rect_area
        if y1 > bottom_line and y2 < top_line:
            satisfied_rect_area_list.append(rect_area)

    x_line = sorted(
        list(set(
            [rect[0] for rect in satisfied_rect_area_list] +
            [rect[2] for rect in satisfied_rect_area_list])))

    y_line = sorted(
        list(set(
            [rect[1] for rect in satisfied_rect_area_list] +
            [rect[3] for rect in satisfied_rect_area_list])),
        reverse=True)

    if not is_regular_table_type:
        y_line.append(bottom_line)

    cell_area_list = [[[] for _ in range(len(x_line) - 1)]
                      for _ in range(len(y_line) - 1)]

    def _add_text_area_into_cell_area_list(_text_area):
        _x1, _y1, _x2, _y2, _ = _text_area
        x_center = (_x1 + _x2) / 2
        y_center = (_y1 + _y2) / 2

        x, y = -1, -1
        for x_r in range(len(x_line) - 1):
            if x_line[x_r] < x_center < x_line[x_r + 1]:
                x = x_r
                break
        if x == -1:
            return None

        for y_r in range(len(y_line) - 1):
            if y_line[y_r] > y_center > y_line[y_r + 1]:
                y = y_r
        if y == -1:
            return None

        return y, x, _text_area

    for text_area in text_area_list:
        result = _add_text_area_into_cell_area_list(text_area)
        if result:
            _y, _x, _text_area = result
            cell_area_list[_y][_x].append(_text_area)

    result_list = []

    for row_data_list in cell_area_list:
        col_result_list = []
        for col_data_list in row_data_list:
            result_text = ''
            if len(col_data_list) != 0:
                col_data_list = sorted(col_data_list,
                                       key=lambda c: (-c[3], c[0]))
                tmp_text_list = [col[4] for col in col_data_list]
                result_text = ''.join(tmp_text_list)

            col_result_list.append(result_text)

        if set(col_result_list) != {''}:
            result_list.append(col_result_list)

    return result_list
