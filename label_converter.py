"""
    Label convertion apis that let you convert label formatting between
    some commonly used formats.
"""
import xml.etree.ElementTree as ET
import pandas as pd


#find bounding box of tables
def not_table(char):
    f = open(f"./not_table_qianzhui_{char}.txt", "r")
    a=[x for x in f]
    data_whole=eval(a[0])
    sort_dic={}
    for k, v in data_whole.items():
        sort_dic[k]=(sorted(v, key=lambda v: v['location'][1]))

    whole_res={}
    for page in sort_dic.keys():
        every_page=sort_dic.get(page)
        page_res=[]
        if len(every_page) > 0:
            if len(every_page)%2==0:
                if every_page[0].get('value')=='%' or every_page[0].get('value')=='#':
                    for i in range(0,len(every_page)-1,2):
                        loc=[]
                        loc.append(every_page[i].get('location')[0])
                        loc.append(every_page[i].get('location')[1])
                        loc.append(1450+250)
                        loc.append(every_page[i+1].get('location')[1])
                        page_res.append(loc)
                if every_page[0].get('value')=='$':
                    loc=[]
                    loc.append(230+250)
                    loc.append(205)
                    loc.append(1450+250)
                    loc.append(every_page[0].get('location')[1])
                    page_res.append(loc)
                    for i in range(1,len(every_page)-1,2):
                        loc=[]
                        loc.append(every_page[i].get('location')[0])
                        loc.append(every_page[i].get('location')[1])
                        loc.append(1450+250)
                        loc.append(every_page[i+1].get('location')[1])
                        page_res.append(loc)
                    loc=[]
                    loc.append(every_page[len(every_page)-1].get('location')[0])
                    loc.append(every_page[len(every_page)-1].get('location')[1])
                    loc.append(1450+250)
                    loc.append(1980)
                    page_res.append(loc)
            else:
                if every_page[0].get('value')=='$':
                    loc=[]
                    loc.append(230+250)
                    loc.append(205)
                    loc.append(1450+250)
                    loc.append(every_page[0].get('location')[1])
                    page_res.append(loc)
                    for i in range(1,len(every_page)-1,2):
                        loc=[]
                        loc.append(every_page[i].get('location')[0])
                        loc.append(every_page[i].get('location')[1])
                        loc.append(1450+250)
                        loc.append(every_page[i+1].get('location')[1])
                        page_res.append(loc)
                if every_page[0].get('value')=='%' or every_page[0].get('value')=='#':
                    for i in range(0,len(every_page)-1,2):
                        loc=[]
                        loc.append(every_page[i].get('location')[0])
                        loc.append(every_page[i].get('location')[1])
                        loc.append(1450+250)
                        loc.append(every_page[i+1].get('location')[1])
                        page_res.append(loc)
                    loc=[]
                    loc.append(every_page[len(every_page)-1].get('location')[0])
                    loc.append(every_page[len(every_page)-1].get('location')[1])
                    loc.append(1450+250)
                    loc.append(1980)
                    page_res.append(loc)
            whole_res[page]=(page_res)
    whole = []
    for page in whole_res.keys():
        obj = []
        for i in range(len(whole_res[page])):
            obj.append({'name': "nottable", 'bndbox': whole_res[page][i]})
        whole.append(obj)
    return whole,whole_res.keys(),whole_res


def table(char):
    f = open(f"./table_qianzhui_{char}.txt", "r")
    a=[x for x in f]
    data_whole=eval(a[0])
    sort_dic={}
    for k, v in data_whole.items():
        sort_dic[k]=(sorted(v, key=lambda v: v['location'][1]))

    whole_res={}
    for page in sort_dic.keys():
        every_page=sort_dic.get(page)
        page_res=[]
        if len(every_page)>0:
            if len(every_page)%2==0:
                if every_page[0].get('value')=='@':
                    for i in range(0,len(every_page)-1,2):
                        loc=[]
                        loc.append(every_page[i].get('location')[0])
                        loc.append(every_page[i].get('location')[1])
                        loc.append(1450+250)
                        loc.append(every_page[i+1].get('location')[1])
                        page_res.append(loc)
                if every_page[0].get('value')=='*':
                    loc=[]
                    loc.append(230+250)
                    loc.append(205)
                    loc.append(1450+250)
                    loc.append(every_page[0].get('location')[1])
                    page_res.append(loc)
                    for i in range(1,len(every_page)-1,2):
                        loc=[]
                        loc.append(every_page[i].get('location')[0])
                        loc.append(every_page[i].get('location')[1])
                        loc.append(1450+250)
                        loc.append(every_page[i+1].get('location')[1])
                        page_res.append(loc)
                    loc=[]
                    loc.append(every_page[len(every_page)-1].get('location')[0])
                    loc.append(every_page[len(every_page)-1].get('location')[1])
                    loc.append(1450+250)
                    loc.append(1980)
                    page_res.append(loc)
            else:
                if every_page[0].get('value')=='*':
                    loc=[]
                    loc.append(230+250)
                    loc.append(205)
                    loc.append(1450+250)
                    loc.append(every_page[0].get('location')[1])
                    page_res.append(loc)
                    for i in range(1,len(every_page)-1,2):
                        loc=[]
                        loc.append(every_page[i].get('location')[0])
                        loc.append(every_page[i].get('location')[1])
                        loc.append(1450+250)
                        loc.append(every_page[i+1].get('location')[1])
                        page_res.append(loc)
                if every_page[0].get('value')=='@':
                    for i in range(0,len(every_page)-1,2):
                        loc=[]
                        loc.append(every_page[i].get('location')[0])
                        loc.append(every_page[i].get('location')[1])
                        loc.append(1450+250)
                        loc.append(every_page[i+1].get('location')[1])
                        page_res.append(loc)
                    loc=[]
                    loc.append(every_page[len(every_page)-1].get('location')[0])
                    loc.append(every_page[len(every_page)-1].get('location')[1])
                    loc.append(1450+250)
                    loc.append(1980)
                    page_res.append(loc)
            whole_res[page]=(page_res)
    whole = []
    for page in whole_res.keys():
        obj = []
        for i in range(len(whole_res[page])):
            obj.append({'name': "nottable", 'bndbox': whole_res[page][i]})
        whole.append(obj)
    return whole,whole_res.keys(),whole_res


def frcnn_label_to_csv(alphas, output_name, base_path):
    df = pd.DataFrame()
    df = pd.DataFrame(columns=['filepath', 'x1', 'y1', 'x2', 'y2', 'class_name'])
    for alpha in alphas:
        whole, key, whole_res = not_table(alpha)
        for number, key in enumerate(whole_res.keys()):
            for i in range(len(whole_res[key])):
                df = df.append(
                    {'filepath': base_path + f'dilation_pad_no_qianzhui_{alpha}_{key}.png', 'x1': whole_res[key][i][0]
                        , 'y1': whole_res[key][i][1], 'x2': whole_res[key][i][2]
                        , 'y2': whole_res[key][i][3], 'class_name': 'nottable'}, ignore_index=True)
        whole, key, whole_res = table(alpha)
        for number, key in enumerate(whole_res.keys()):
            for i in range(len(whole_res[key])):
                df = df.append(
                    {'filepath': base_path + f'dilation_pad_no_qianzhui_{alpha}_{key}.png', 'x1': whole_res[key][i][0]
                        , 'y1': whole_res[key][i][1], 'x2': whole_res[key][i][2]
                        , 'y2': whole_res[key][i][3], 'class_name': 'table'}, ignore_index=True)
    df.to_csv(f'{output_name}.txt', header=None, index=None, sep=',')


def _get_object_dicts(json_shapes):
    """
    Helper function.
    Get the object label along with its bounding box coordinates.

    Args:
        json_shapes ([dict]): dict containing all the object info within one image

    Returns:
        [dict]: dict containing object info in a easy-to-access format
    """

    objects = []
    for js in json_shapes:
        obj = {}
        obj['name'] = js['label']
        obj['bndbox'] = [
            str(n) for n in [
                js['points'][0][0],
                js['points'][0][1],
                js['points'][2][0],
                js['points'][2][1]
            ]
        ]

        objects.append(obj)
    return objects


def _create_new_xml_file(folder, filename, path, h, w, objects, xml_out_path):
    """

    Helper function.
    Create a new xml file according to the provided info.

    Args:
        folder ([str]): folder name in which training images are stored.
        filename ([str]): image filename.
        path ([str]): absolute path of the image file starting from root.
        h ([int]): image height.
        w ([int]): image width.
        objects ([dict]): dictionary containing object labels and bounding boxes.
        xml_out_path ([str]): path to store the new xml file and file name
    """

    root = ET.Element('annotation')
    ET.SubElement(root, 'folder').text = folder
    ET.SubElement(root, 'filename').text = filename
    ET.SubElement(root, 'path').text = path

    source = ET.SubElement(root, 'source')
    ET.SubElement(source, 'database').text = 'Unknown'

    size = ET.SubElement(root, 'size')
    ET.SubElement(size, 'width').text = str(h)
    ET.SubElement(size, 'height').text = str(w)
    ET.SubElement(size, 'depth').text = '3'

    ET.SubElement(root, 'segmented').text = '0'

    for obj in objects:
        new_obj = ET.SubElement(root, 'object')
        ET.SubElement(new_obj, 'name').text = obj['name']
        ET.SubElement(new_obj, 'pose').text = 'Unspecified'
        ET.SubElement(new_obj, 'truncated').text = '0'
        ET.SubElement(new_obj, 'difficult').text = '0'
        bndbox = ET.SubElement(new_obj, 'bndbox')

        ET.SubElement(bndbox, 'xmin').text = str(obj['bndbox'][0])
        ET.SubElement(bndbox, 'ymin').text = str(obj['bndbox'][1])
        ET.SubElement(bndbox, 'xmax').text = str(obj['bndbox'][2])
        ET.SubElement(bndbox, 'ymax').text = str(obj['bndbox'][3])

    tree = ET.ElementTree(root)
    tree.write(xml_out_path)


def _convert_one_from_json_to_xml(
        xml_dir,
        img_dir,
        path_root,
        img_h,
        img_w,
        json_file_path
):
    """
    Convert one json formated label file to xml

    Args:
        xml_dir ([str]): path to store the xml label file.
        img_dir ([str]): image folder name in which training images are stored.
        path_root ([str]): absolute path to the image folder.
        img_h ([type]): image height.
        img_w ([type]): image width.
        json_file_path ([type]): input json formated label file.
    """

    # try to catch univodeDecodeError while opening json file
    # spaces or Chinese characters in file name may cause this
    try:
        with open(json_file_path, 'r') as fr:
            contents = json.loads(fr.read())
    except UnicodeDecodeError:
        print(
            'UnicodeDecodeError encountered while reading {}.\n'
            'Remove possible white spaces or Chinese characters any try again'
                .format(json_file_path)
        )
        return

    try:
        # get the corresponding image file name
        image_file_name = contents['imagePath']

        froot = os.path.splitext(image_file_name)[0]
        abs_image_path = os.path.join(path_root, image_file_name)

        xml_file_name = froot + '.xml'
        xml_out_path = os.path.join(xml_dir, xml_file_name)

        obj_dict = _get_object_dicts(contents['shapes'])
    except KeyError:
        # if the required key cannot be found in this json file
        # then this is an invalid json label
        print('Invalid json file detected. {}\n'
              'Some required info cannot be found.'.format(json_file_path))
        return
    except IndexError:
        print('Invalid json file detected. {}\n'
              'Some bounding box coordinates are invalid.'
              .format(json_file_path))
        return

    _create_new_xml_file(
        img_dir,
        image_file_name,
        abs_image_path,
        img_h,
        img_w,
        obj_dict,
        xml_out_path
    )


def convert_from_json_to_xml(
        json_dir,
        xml_dir,
        img_h,
        img_w,
        image_dir,
        path_root
):
    """
    Convert all the json formatted label files in the given directory
    to xml format with required parameters.

    Args:
        json_dir ([str]): path to the input directory in which
                          all the input json label files are stored.
        xml_dir ([str]): path in which
                         all the output xml label files are stored.
        img_h ([int]): image height parameter in the xml label file.
        img_w ([int]): image width parameter in the xml label file.
        image_dir ([str]): image folder parameter in the xml label file
        path_root ([str]): absolute path of the image folder parameter,
                           end with the image folder.

    Raises:
        TypeError: image size parameters should be int.
        TypeError: path parameters should be str.
        ValueError: image size parameters should be positive.
    """

    _check_input_dir(json_dir)
    _check_output_dir(xml_dir)

    if (not isinstance(img_h, int)) or (not isinstance(img_w, int)):
        raise TypeError('Image h and w both should be int.')

    if img_h < 0 or img_w < 0:
        raise ValueError('Image h and w both should be positive')

    if (not isinstance(image_dir, str)) or (not isinstance(path_root, str)):
        raise TypeError('Path parameters should be str.')

    # get all the files with a json extension
    json_file_list = glob.glob('{}/*.json'.format(json_dir))

    # create a wrapper function to wrap the _convert_one_from_json_to_xml
    # function, with 5 of its parameters prefilled.
    func = partial(
        _convert_one_from_json_to_xml,
        xml_dir,
        image_dir,
        path_root,
        img_h,
        img_w
    )

    # get the number of cores in cpu
    num_of_cores = multiprocessing.cpu_count()

    # create a multi-processing pool and map the input path list to
    # the wrapped function to let it feed the input to different cores
    # automatically.
    with multiprocessing.Pool(processes=num_of_cores) as pool:
        pool.map(func, json_file_list)


def _convert_one_from_xml_to_txt(output_dir, xml_file_path):
    """
    Convert one xml format label file to txt format
    and save the txt file to the output directory

    Args:
        output_dir ([str]): path to the output directory
                            to store output txt files
        xml_file_path ([str]): path to the input xml format label file
    """

    # first get the file name, and then get the file name root
    filename_root = os.path.splitext(os.path.split(xml_file_path)[1])[0]

    # get the path to the output txt file
    destination_path = os.path.join(output_dir, filename_root + '.txt')

    try:
        # try to parse the xml tree from the input path
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
    except ET.ParseError:
        # in case of a parse error, throw exception to indicate which file
        # caused the exception and return.
        print('Possible invalid xml file detected,\n'
              'Cannot parse file {}'.format(xml_file_path))
        return

    # read all the required info from the xml file
    img_path = root.find('path').text
    obj_list = []
    for obj in root.iter('object'):
        obj_list.append(
            [
                obj.find('bndbox').find('xmin').text,
                obj.find('bndbox').find('ymin').text,
                obj.find('bndbox').find('xmax').text,
                obj.find('bndbox').find('ymax').text,
                obj.find('name').text
            ]
        )

    # insert absolute path at the front of every record of object
    [l.insert(0, img_path) for l in obj_list]

    # write the records out to the destination txt file
    with open(destination_path, 'w') as fw:
        for obj in obj_list:
            fw.write(','.join(obj) + '\n')


def convert_from_xml_to_txt(xml_dir, output_dir):
    """
    Convert all the xml formatted label files in the given directory
    to txt format.

    Args:
        xml_dir ([str]): path to the input directory
                         in which all the xml format label files are stored
        output_dir ([str]): path to the output directory
                            to store output txt files

    Sample Output Format:
        /abs/path/to/the/training image,xmin,ymin,xmax,ymax,class
    """

    _check_input_dir(xml_dir)
    _check_output_dir(output_dir)

    # retrieve all the files with xml extension from the input directory
    xml_file_list = glob.glob('{}/*.xml'.format(xml_dir))

    # create a wrapper function to wrap the _convert_one_from_xml_to_txt
    # function, with 1 of the parameters prefilled.
    func = partial(
        _convert_one_from_xml_to_txt,
        output_dir
    )

    # get the number of available cpu cores
    num_of_cores = multiprocessing.cpu_count()

    # create a multi-processing pool and map the input path list to
    # the wrapped function to let it feed the input to different cores
    # automatically.
    with multiprocessing.Pool(processes=num_of_cores) as pool:
        pool.map(func, xml_file_list)


def _get_object_list_from_txt_list(txt_list):
    objects = []
    for label in txt_list:
        obj = {}
        obj['name'] = label[5].split('\n')[0]
        obj['bndbox'] = [str(n) for n in label[1:5]]

        objects.append(obj)
    return objects


def _convert_one_from_txt_to_xml(output_dir, txt_file_path):
    filename = os.path.splitext(os.path.split(txt_file_path)[1])[0]
    output_xml_path = os.path.join(output_dir, filename + '.xml')

    with open(txt_file_path, 'r') as fr:
        lines = [l.split(',') for l in fr.readlines()]
    if len(lines) == 0:
        return
    img_path = lines[0][0]
    img_name = os.path.split(img_path)[1]
    filename_root = os.path.splitext(img_name)[0]
    img_folder = img_path.split('/')[-2]

    #     img = cv2.imread(img_path, 0)
    #     if img is None:
    #         raise ValueError('Cannot find image {}.'.format(img_path))
    #     h, w, _ = img.shape
    h = 100
    w = 100
    objects = _get_object_list_from_txt_list(lines)
    output_xml_path = os.path.join(output_dir, filename_root + '.xml')

    _create_new_xml_file(
        img_folder,
        img_name,
        img_path,
        h,
        w,
        objects,
        output_xml_path
    )


def convert_from_txt_to_xml(txt_dir, output_dir):
    _check_input_dir(txt_dir)
    _check_output_dir(output_dir)

    txt_file_list = glob.glob('{}/*.txt'.format(txt_dir))

    # create a wrapper function to wrap the _convert_one_from_txt_to_xml
    # function, with 1 of the parameters prefilled.
    func = partial(
        _convert_one_from_txt_to_xml,
        output_dir
    )

    # get the number of available cpu cores
    num_of_cores = multiprocessing.cpu_count()

    # create a multi-processing pool and map the input path list to
    # the wrapped function to let it feed the input to different cores
    # automatically.
    with multiprocessing.Pool(processes=num_of_cores) as pool:
        pool.map(func, txt_file_list)


'''
to create xml file for yolo3
'''
# alphas=['a','b','c','d']
# for alpha in alphas:
#     whole=obj_location(f'qianzhui_{alpha}')[0]
#     keys=obj_location(f'qianzhui_{alpha}')[1]
#     for i,key in enumerate(keys):
#         _create_new_xml_file('./dilation_train/', f'dilation_pad_qianzhui_{alpha}_{key}.png', './dilation_train/', 2200, 2200, whole[i], f'./xml_train/dilation_train_{alpha}_{key}.xml')
#
# whole=obj_location(f'qianzhui_e')[0]
# keys = obj_location(f'qianzhui_e')[1]
# for i, key in enumerate(keys):
#     _create_new_xml_file('./dilation_test/', f'dilation_pad_qianzhui_e_{key}.png', './dilation_test/', 2200, 2200, whole[i], f'./xml_test/dilation_test_{key}.xml')
#


'''
to create csv file for faster-rcnn
'''
# frcnn_label_to_csv(alphas=['a', 'b', 'c', 'd', 'e', 'f'], output_name='train_label', base_path='./train_image/')
frcnn_label_to_csv(alphas=['a', 'b'], output_name='train_label_subset', base_path='./train_image_subset/')
