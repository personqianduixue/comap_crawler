"""
爬取美赛获奖证书,并以控制号命名
只运行一次部分下载会失败，需要运行多次，确保全部下载
"""
import os

import requests
import pandas as pd
from multiprocessing import Process

class CMcmCertificateCrawler():
    def __init__(self,contol_nmuber):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/73.0.3683.103 Safari/537.36'
        }
        self.control_number = contol_nmuber

    def FGetResponse(self):
        url = "http://www.comap-math.com/mcm/2022Certs/" + str(self.control_number) + ".pdf"
        response = requests.get(url=url, headers=self.headers)
        # print(response.status_code)
        return response

    def FSavePDF(self, control_number):
        # 下载证书PDF
        try:
            path = "./paper/" + str(control_number) + ".pdf"
            response = self.FGetResponse()
            # print(response.status_code)
            if response.status_code != 404:
                with open(path, 'wb') as f:
                    f.write(response.content)
                    print(str(control_number) + ".pdf" + "存储成功")
            else:
                print(control_number,' -- 404')
        except Exception:
            print("Exception")

def download(start,end):
    for control_number in range(start,end):
        control_number = '%05d' % control_number
        control_number = 2200000 + int(control_number)
        mcc = CMcmCertificateCrawler(control_number)
        mcc.FSavePDF(control_number)

def downloadlist(control_number_list):
    for control_number in control_number_list:
        mcc = CMcmCertificateCrawler(control_number)
        mcc.FSavePDF(control_number)


if __name__ == '__main__':
    all_control_list = []
    for control_number in range(1, 30000):
        control_number = '%05d' % control_number
        control_number = 2200000 + int(control_number)
        all_control_list.append(control_number)

    dir = './paper/'
    download_filelist = os.listdir(dir)
    for filename in download_filelist:
        filenum = int(filename[0:7])
        print(filenum)
        filesize = os.path.getsize(dir + filename)
        if filesize:
            all_control_list.remove(filenum)

    step = 30
    for i in range(0,len(all_control_list),step):
        start = i
        end = i+step-1
        control_numbers = all_control_list[start:end]
        p = Process(target=downloadlist, args=(control_numbers,))
        p.start()
