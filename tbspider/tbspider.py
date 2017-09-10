#coding=utf-8
'''
    Module document
'''
import http
import requests
import urllib
import json
import chardet
import traceback
import sys

class TBspider(object):
    '''
    crawler for taobao
    '''

    def __init__(self,headers=None,cookies=None,proxies=None,**kwargs):
        """init information"""

        self.search_s = ''
        self.start_page = 1
        self.start_url = 'https://s.taobao.com/search'
        self.comment_url = 'https://rate.tmall.com/list_detail_rate.htm'
        self._sort = 'default'
        self._items = []
        self._detail_urls = None
        self._comment_urls = None
        self.headers = headers or http.headers
        self.cookies = cookies or http.cookies
        self.proxies = proxies or http.proxy_pool[0]
        self.__dict__.update(kwargs)


    @property
    def items(self):
        """get self._items"""
        return self._items


    @property
    def sort(self):
        """get sort type"""
        return self._sort


    @sort.setter
    def sort(self,sort_type):
        """
        set sort type:
            ;default
            ;renqi-desc/renqi-asc
            ;sale-desc/sale-asc
            ;credit-desc/credit-asc
            ;price-desc/price-asc
        """

        types = ['default','renqi-desc','renqi-asc','sale-desc','sale-asc',
                 'credit-desc','credit-asc','price-desc','price-asc']
        if sort_type not in types:
            raise TypeError("No such sort_type '%s'"%sort_type)
        self._sort = sort_type


    @property
    def detail_urls(self):
        if self._detail_urls is None:
            self._detail_urls = self.grab_detail_urls()
        return self._detail_urls


    @detail_urls.setter
    def detail_urls(self,urls):
        self._detail_urls = urls


    @property
    def comment_urls(self):

        if self._comment_urls is None:
            self._comment_urls = self.grab_comment_urls()
        return self._comment_urls


    @comment_urls.setter
    def comment_urls(self,urls):
        self._comment_urls = urls


    def grab_items(self,max_page=None,point_page=None):
        """
        get items from pages,each page contain 12 items
        max_page: get items from page which <max_page
        point_page: get items from the appoint page
        ::if set point_page , max_page is invalid
        return items list
        """

        if max_page is None and point_page is None:
            raise ValueError('grab_items() takes at least 1 argument (0 given)')

        data = {'m':'customized',
                'q':self.search_s,
                'sort':self.sort
                }

        if point_page is None:
            while(self.start_page <= max_page):
                data['s'] = str((self.start_page-1) * 12)
                page_item = self.request(self.start_url, callback=self.items_parse, data=data)
                self._items.extend(page_item)
                self.start_page = self.start_page + 1
        else:
            data['s'] = str((point_page - 1) * 12)
            page_item = self.request(self.start_url, callback=self.items_parse, data=data)
            self._items.extend(page_item)

        return self.items


    def comments_spider(self,item):
        """comments spider """

        ct_url = self.comment_url
        callback_func = self.comments_parse(item)

        data = {'itemId':item['nid'],
                'sellerId':item['user_id'],
                'order':3,
                'append':0,
                'currentPage':1}

        resp = self.request(ct_url,data=data,callback=(lambda x:x))

        dt = json.loads('{%s}'%resp.content.strip('\n\r'),encoding='GB18030')
        lastpage = dt['rateDetail']['paginator']['lastPage']


        page_one_comments = callback_func(resp)

        def grab_comments(max_page=None,point_page=None):
            comments = []
            if max_page is None and point_page is None:
                raise ValueError('grab_comments() takes at least 1 argument (0 given)')

            if point_page == 1  and not comments == []:
                comments.extend(page_one_comments)
                return comments

            if point_page is not None:
                data.update({'currentPage':point_page})
                response = self.request(ct_url,data=data,callback=callback_func)
                comments.extend(response)
                return comments

            pages = max_page if max_page<=lastpage else lastpage
            for page in range(1,pages+1):
                if page == 1:
                    comments.extend(page_one_comments)
                else:
                    comments.extend(grab_comments(None,page))
            return comments

        return grab_comments


    def request(self,url,callback=None,method='get',data=None):
        """request for search return page iteration　of commodity"""

        if callback is not None and not callable(callback):
            raise ValueError('callback must be a callable, got %s' % type(callback).__name__)

        method = method.upper()
        response = None

        if method == 'GET':
            try:
                response = requests.get(url,cookies=self.cookies,headers=self.headers,
                                        params=data,proxies=self.proxies)
            except Exception,e:
                print "PROXY:%s %s URL:%s ERROR"%(self.proxies,method,url)
                traceback.print_exc()

        elif method == 'POST':
            try:
                response = requests.post(url,cookies=self.cookies,headers=self.headers,
                                        data=data,proxies=self.proxies)
            except Exception,e:
                print "PROXY:%s %s URL:%s ERROR" % (self.proxies, method, url)
                traceback.print_exc()

        print 'PROXY:%s /%s URL:%s \n Response:URL %s /STATUS_CODE:%s'%(self.proxies,method,url,response.url,response.status_code)
        return callback(response)


    def items_parse(self,response):
        """parse for response data"""

        #date = time.strftime('%Y%m%d%H%M',time.localtime(time.time()))
        auctions = response.json()['API.CustomizedApi']['itemlist']['auctions']
        items = [self.select_item(ac) for ac in auctions]
        return items


    def comments_parse(self,item):
        """parse for response data"""

        def parse(response):
            try:
                json_obj = json.loads('{%s}' % response.content.strip('\n\r'), encoding='GB18030')
            except Exception as e:
                print e
                print response.content
                sys.exit()

            rateList = json_obj['rateDetail']['rateList']
            if rateList == []:
                return []
            comments = [self.select_comment(rl,item) for rl in rateList]
            return comments
        return parse


    def select_item(self,auction):
        """select item from auction"""

        item_fields = ('nid','category','raw_title','detail_url','view_price',
                  'view_fee','item_loc','view_sales','comment_count','user_id','nick','comment_url','shopLink')
        item = dict([(i,auction[i]) for i in item_fields])
        return item


    def select_comment(self,ratelist,item):
        """select comment from auction"""

        inline_item_fields = ('nid',)
        comment_fields = ('rateContent','auctionSku','rateDate')
        comment = dict([(c,ratelist[c]) for c in comment_fields])
        comment.update(dict([(i,item[i]) for i in inline_item_fields]))
        return comment


    def grab_detail_urls(self):
        return [i['detail_url'] for i in self.items]


    def grab_comment_urls(self):
        """grab detail urls from items"""

        comment_urls = map(lambda x:self.comment_url+'?'+urllib.urlencode({'itemId':x['nid'],
                                                  'sellerId':x['user_id'],
                                                  'order':3,
                                                  'append':0}),self.items)
        return comment_urls




    def save_items(self,conn):
        """save items in mysql"""

        cursor = conn.cursor()
        for item in self.items:
            sql = """insert into summary(nid,category,raw_title,detail_url,view_price,
            view_fee,item_loc,view_sales,comment_count,user_id,nick,comment_url,shoplink) 
            values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')""" % \
                  (item['nid'],item['category'],item['raw_title'],item['detail_url'],
                   item['view_price'],item['view_fee'],item['item_loc'],item['view_sales'],
                   item['comment_count'],item['user_id'],item['nick'],item['comment_url'],item['shopLink'])
            try:
                cursor.execute(sql)
            except:
                conn.rollback()

        conn.commit()
        conn.close()


    def print_items(self,datas=None):
        """print items"""

        items = datas if datas else self.items
        for i in items:
            print "%-18s %-50s %-10s %-10s %-100s" % (i['nick'], i['raw_title'], i['view_price'], i['view_sales'],i['comment_url'])




if __name__ == '__main__':
    pass
