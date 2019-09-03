"""
convert pdf to png
"""



from pdf2image import convert_from_path

alphas=['a','b','c','d','e','f']
for alpha in alphas:
    pages2 = convert_from_path(f'no_qianzhui_{alpha}.pdf')
    for i in range(0, len(pages2)):
        pages2[i].save(f'./train_image/no_qianzhui_{alpha}_{i}.png', 'PNG')

# pages3 = convert_from_path(f'qianzhui_f.pdf')
# for i in range(0, len(pages3)):
#     pages3[i].save(f'./test_image/qianzhui_f_{i}.png', 'PNG')


# pages2 = convert_from_path('/Users/zjiang032/Downloads/Financial Statement Sample - normal/Financial_report1_normal.pdf')
# for i in range(0, len(pages2)):
#     pages2[i].save(f'/Users/zjiang032/Downloads/Financial Statement Sample - normal/Financial_report/Financial_report1_normal{i}.png', 'PNG')
