#coding:utf-8
import time
import sys
import json
import requests
import pymysql
import multiprocessing
from functools import wraps
from spiders.tbspider import tbspider

reload(sys)
sys.setdefaultencoding("utf-8")

def calc_time(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        st = time.time()
        ret = func(*args,**kwargs)
        print '%-12s:%.3f sec'%(func.func_name,time.time()-st)
        return ret
    return wrapper


def crawl_item(search=None,sort_type=None,start_p=None,max_p=None,point_p=None):

    tb = tbspider.TBspider()
    tb.start_url = "https://s.taobao.com/api"
    tb.search_s = search if search else 'something'
    tb.sort = sort_type if sort_type else "renqi-asc"
    tb.start_page = start_p if start_p else tb.start_page
    tb.grab_items(max_page=max_p,point_page=point_p)
    tb.print_items()
    return tb.items


def crawl_comment(item,comment_pages=None):
    tb = tbspider.TBspider()
    spider = tb.comments_spider(item)
    return spider(max_page=comment_pages)


@calc_time
def multispider_item(pages=None):

    mng = multiprocessing.Manager()
    item_list = mng.list()

    if pages == 0:
        return

    pool = multiprocessing.Pool()

    for p in range(1,pages+1):
        pool.apply_async(crawl_item,('vivo x9','sale-desc',None,None,p),callback=item_list.extend)

    pool.close()
    pool.join()
    return item_list


@calc_time
def multispider_comment(items,comment_pages):

    mng = multiprocessing.Manager()
    comment_list = mng.list()
    pool = multiprocessing.Pool()

    for item in items:
        pool.apply_async(crawl_comment, (item, comment_pages), callback=comment_list.extend)

    pool.close()
    pool.join()
    return comment_list



def result_to_mysql(tb):
    """doc"""
    conn = pymysql.connect(host='localhost',
                           user='lsg01',
                           passwd='',
                           db='taobao',
                         charset='utf8')
    tb.save_items(conn)



if __name__ == "__main__":

    items = multispider_item(pages=1)
    comments = multispider_comment(items,comment_pages=1)
    for i in comments:
        print json.dumps(i,ensure_ascii=False,indent=2)











