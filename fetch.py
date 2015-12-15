# -*- coding: utf-8 -*-
import requests as rq
import re
import pandas as pd
import json
import sys
import datetime

url='http://world.tmall.com/item/44320847678.htm?spm=a220m.1000858.0.0.K7jhC4&id=44320847678&is_b=1&cat_id=2&q=%BC%D7%C8%A9'
URL_BASE= 'https://rate.tmall.com/list_detail_rate.htm?'

SPU_PREFIX='spuId='
SELLER_PREFIX='sellerId='
ITEM_PREFIX='itemId='
AND='&'
ORDER_BY_TIME='order=1'
APPEND='append=0'
CONTENT='content=1'
BAD_TAG='tagId=620'
PAGE='currentPage='
result=''
index = 0
POS='posi=-1'
PICTURE='picture=0'

def getSpuId(data):
    sup_m= re.search(SPU_PREFIX+'\d*',data)
    if sup_m:
        return str(sup_m.group(0))
    else:
        return None

def getSellerId(data):
    seller_m = re.search(SELLER_PREFIX+'\d*',data)
    if seller_m:
        return str(seller_m.group(0))
    else:
        return None

def getItemId(data):
    item_m = re.search(ITEM_PREFIX+'\d*',data)
    if item_m:
        return str(item_m.group(0))
    else:
        return None
def getPage(page_id,url):
    comments = rq.get(url+AND+PAGE+str(page_id))
    content = re.findall('\"rateList\":(\[.*?\])\,\"tags\"',comments.text.encode('utf-8'))[0]
    myjson = json.loads(content)
    page_content =''
    if len(myjson) == 0 :
        print "no more data " ,page_id
        return None
    for item in myjson:
        #if len(item['rateContent'].encode('utf-8')) <400:
        #    continue
        global index
        index += 1
        page_content += str(index)+' :'
        page_content += item['rateDate']
        page_content += item['rateContent']
        page_content += '</br>'
    return page_content



def printPages(page,url):
    pages=''
    for i in range(1,page+1):
        page=getPage(i,url)
        if page:
            pages+=page
        else:
            break;
    return pages


def getComments(url,bad=False,page=5):
    myweb = rq.get(url)
    raw = myweb.text
    spuId = getSpuId(raw)
    sellerId = getSellerId(raw)
    itemId = getItemId(raw)
    url_base = URL_BASE+spuId+AND+sellerId+AND+itemId +AND + ORDER_BY_TIME+AND+APPEND+AND+CONTENT+AND + POS + AND+PICTURE
    if bad:
        url_base += AND+BAD_TAG
    cms = printPages(page,url_base)
    #print cms.encode('utf-8')
    cmsu = cms.encode('utf-8')
    return cmsu


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'fetch2.py url'
        sys.exit()
    #get the bad comments by time
    print getComments(sys.argv[1],True,2)


