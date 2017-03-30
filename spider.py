#encoding=utf-8
import requests
import time
import re
from selenium import webdriver
import sys
import csv
import warnings
warnings.filterwarnings("ignore")
stdi,stdo,stde=sys.stdin,sys.stdout,sys.stderr
reload(sys)
sys.setdefaultencoding('utf-8',) 
sys.stdin,sys.stdout,sys.stderr=stdi,stdo,stde
def loadCSVfile(file):
    csv_reader = csv.reader(open(file))
    return csv_reader
def get_iplist(filename,page,sort):
    data=[]
    driver = webdriver.PhantomJS()
    csvfile = file(filename, 'wb')
    for r in range(1,page+1):
        print 'Page',
        print r
        a=driver.get('http://www.kuaidaili.com/free/'+str(sort)+'/'+str(r))
        tr=[]
        while tr==[]:
            hm=driver.page_source
            tr=re.findall('<tr>(.*?)</tr>',hm,re.S)
        for each in tr:
            try:
                ip=re.findall('<td data\-title="IP">(.*?)</td>',each,re.S)[0]
                port=re.findall('<td data\-title="PORT">(.*?)</td>',each,re.S)[0]
                tp=re.findall('<td data-title="'+'类型'.decode('utf8')+'">(.*?)</td>',each,re.S)[0]
                loc=re.findall('<td data-title="'+'位置'.decode('utf8')+'">(.*?)</td>',each,re.S)[0]
                speed=re.findall('<td data-title="'+'响应速度'.decode('utf8')+'">(.*?)</td>',each,re.S)[0]
                last=re.findall('<td data-title="'+'最后验证时间'.decode('utf8')+'">(.*?)</td>',each,re.S)[0]
                print ip,
                print port,
                print tp,
                print loc,
                print speed,
                print last
                data.append((ip,port,tp,loc,speed,last))
            except Exception as err:
                print err
    driver.quit()
    writer = csv.writer(csvfile)
    writer.writerows(data)
    csvfile.close()

def filter_iplist(filename,newfilename,timeout):
    proxylist=loadCSVfile(filename)
    successlist=[]
    for each in proxylist:
        try:
            address='http://'+str(each[0])+':'+str(each[1])
            proxies=[]
            proxies.append({'http':address})
            t=requests.get('http://www.jd.com',proxies=proxies[0],timeout=timeout,verify=False).text
            print 'Success', each[0] ,':', each[1]
            successlist.append((each[0],each[1],each[2],each[3],each[4],each[5]))
        except Exception as err:
            print 'Failed', each[0] ,':', each[1]
    csvfile = file(newfilename, 'wb')
    writer = csv.writer(csvfile)
    writer.writerows(successlist)
    csvfile.close()     
get_iplist('ip.csv',3,'inha') #参数为（文件名，页数，代理类别）；代理类别包含4种(inha:国内高匿,intr:国内普通,outha:国外高匿,outtr:国外普通
filter_iplist('ip.csv','new.csv',2)  #过滤出有效IP并存储为new.csv 参数为（文件名，过滤后的文件名，超时判定秒数）










    
