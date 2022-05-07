"""
美赛获奖证书信息OCR
"""

import fitz
import PIL
import pytesseract
import os
from multiprocessing import Process
from multiprocessing import Queue
import sys
import logging
import io
import re

pytesseract.pytesseract.tesseract_cmd = 'E:/prog/TesseractOCR/tesseract.exe'


def pdf2text(pdfPath, zoom_x=6, zoom_y=6, rotation_angle=0):
    students = ['']
    university = ''
    prize = ''
    try:
        # 打开PDF文件
        pdf = fitz.open(pdfPath)
        # 逐页读取PDF
        for pg in range(0, pdf.pageCount):
            page = pdf[pg]
            rect = page.rect
            clip = fitz.Rect(rect.width * 0.25, rect.height * 0.27,
                             rect.width * 0.8, rect.height * 0.7)
            trans = fitz.Matrix(zoom_x, zoom_y).prerotate(rotation_angle)
            pix = page.get_pixmap(matrix=trans, alpha=False, clip=clip)
            img = PIL.Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text = pytesseract.image_to_string(img)
            text = text.split('\n')
            text = [s for s in text if s]
            try:
                advisor_index = text.index('With Student Advisor')
            except:
                try:
                    advisor_index = text.index('With Faculty Advisor')
                except:
                    advisor_index = text.index('Was Designated As') - 3
            try:
                univ_index = text.index('Was Designated As') - 1
                students = text[0:advisor_index]
                university = text[univ_index]
            except:
                students = text[0:3]
                university = text[5]
            prize = text[-1]
            # pix.save(imgPath + str(pg) + ".png")
        pdf.close()
    except:

        print(pdfPath, 'File Exception')

    return students, university, prize


def savetext(start, end, count):
    global logger
    all_data = ''
    huake_data = ''
    for control_number in range(start, end):
        control_number = '%05d' % control_number
        control_number = 2200000 + int(control_number)
        path = "./paper/" + str(control_number) + ".pdf"
        if os.path.exists(path):
            students, university, prize = pdf2text(path)
            students = ','.join(students)
            row = '%s,%s,%s\n' % (students, university, prize)
            if prize:
                num_row = '%s,%s' % (control_number, row)
                num_row = num_row.encode('gbk', 'backslashreplace').decode('gbk', 'backslashreplace')
                try:
                    print(num_row)
                except:
                    print(control_number, ' -- gbk encoding error')

                all_data += num_row
                if university == 'Huazhong University of Science and Technology':
                    huake_data += num_row

    with open('./all/all' + str(count) + '.txt', 'w', encoding='utf-8') as al:
        # all_data = all_data.encode('utf-8')
        al.write(all_data)
        print('./all/all' + str(count) + '.txt save sucessfully')
    with open('./huake/huake' + str(count) + '.txt', 'w', encoding='utf-8') as huake:
        # huake_data = huake_data.decode('utf-8')
        huake.write(huake_data)
        print('./huake/huake' + str(count) + '.txt save sucessfully')

# def savetextlist(lists,count):
#     all_data = ''
#     huake_data = ''
#     for control_number in lists:
#         path = "./paper/" + str(control_number) + ".pdf"
#         if os.path.exists(path):
#             students, university, prize = pdf2text(path)
#             students = ','.join(students)
#             row = '%s,%s,%s\n' % (students, university, prize)
#             if prize:
#                 num_row = '%s,%s' % (control_number, row)
#                 num_row = num_row.encode('gbk', 'backslashreplace').decode('gbk', 'backslashreplace')
#                 try:
#                     print(num_row)
#                 except:
#                     print(control_number, ' -- gbk encoding error')
#
#                 all_data += num_row
#                 if university == 'Huazhong University of Science and Technology':
#                     huake_data += num_row
#     with open('./all/all_add' + str(count) + '.txt', 'w', encoding='utf-8') as al:
#         # all_data = all_data.encode('utf-8')
#         al.write(all_data)
#         print('./all/all_add' + str(count) + '.txt save sucessfully')
#     with open('./huake/huake_add' + str(count) + '.txt', 'w', encoding='utf-8') as huake:
#         # huake_data = huake_data.decode('utf-8')
#         huake.write(huake_data)
#         print('./huake/huake_add' + str(count) + '.txt save sucessfully')



def txtjoint(dir):
    files = os.listdir(dir)
    res = ''
    for file in files:
        with open(dir + file, "r", encoding='utf-8') as f:
            content = f.read()
            res += content

    with open(dir + "all.txt", "w", encoding='utf-8') as outFile:
        outFile.write(res)
        outFile.close()


if __name__ == '__main__':
    step = 1000
    count = 1
    for i in range(1, 30000, step):
        start = i
        end = i + step - 1
        p = Process(target=savetext, args=(start, end, count))
        p.start()
        count += 1

    # 合并文件
    all_dir = "./all/"
    huake_dir = './huake/'
    txtjoint(all_dir)
    txtjoint(huake_dir)

    # with open('log.log','r') as f:
    #     alltxt = f.read()
    #     fail_lists = re.findall('./paper/(\d*?).pdf File Exception',alltxt,re.S)
    #
    # with open('fail_lists.txt','w') as f:
    #     f.write('\n'.join(fail_lists))
    # step = 20
    # count = 1
    # for i in range(1, len(fail_lists), step):
    #     start = i
    #     end = i + step - 1
    #     lists = fail_lists[start:end]
    #     p = Process(target=savetextlist, args=(lists,count,))
    #     p.start()
    #     count += 1
