#coding=utf-8
'''
    Module document
'''
import http
import requests
from multiprocessing import Queue

class TBspider(object):
    '''
    crawler for taobao
    '''

    def __init__(self,headers=None,cookies=None,proxy=None,**kwargs):
        """init information"""

        self.search_s = ''
        self.start_page = 1
        self.start_url = 'https://s.taobao.com/search'
        self._sort = 'default'
        self._items = []
        self._items_q = Queue()
        self._comment_urls = []
        self.headers = headers or http.headers
        self.cookies = cookies or http.cookies
        self.proxy = proxy or http.proxy
        self.__dict__.update(kwargs)


    @property
    def items(self):
        """get self._items"""
        if self._items == []:
            while(True):
                try:
                    self._items.extend(self._items_q.get_nowait())
                except:
                    break
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
    def comment_urls(self):
        if self._comment_urls == []:
            self._comment_urls = self.grab_urls_from_items()
        return self._comment_urls


    @comment_urls.setter
    def comment_urls(self,urls):
        self._comment_urls = urls


    def grab_items(self,max_page=None,point_page=None):
        """
        get items from pages
        :param max_page: get items from page which <max_page
        :param point_page: get items from the appoint page
        if set point_page , max_page is invalid
        :return: items list
        """

        if max_page is None and point_page is None:
            raise ValueError('grab_items() takes at least 1 argument (0 given)')

        data = {'m':'customized',
                'q':self.search_s,
                'sort':self.sort
                }
        items_t = []
        if point_page is None:
            while(self.start_page <= max_page):
                data['s'] = str((self.start_page-1) * 12)
                page_item = self.request(self.start_url, callback=self.parse, data=data)
                items_t.extend(page_item)
                self._items_q.put(page_item)
                self.start_page = self.start_page + 1
        else:
            data['s'] = str((point_page - 1) * 12)
            page_item = self.request(self.start_url, callback=self.parse, data=data)
            items_t.extend(page_item)
            self._items_q.put(page_item)

        return items_t


    def request(self,url,callback=None,method='get',data=None):
        """request for search return page iteration　of commodity"""

        if callback is not None and not callable(callback):
            raise ValueError('callback must be a callable, got %s' % type(callback).__name__)

        method = method.upper()
        response = None

        if method == 'GET':
            response = requests.get(url,cookies=self.cookies,headers=self.headers,params=data)
        elif method == 'POST':
            response = requests.post(url,cookies=self.cookies,headers=self.headers,data=data)
        print 'url:%s status_code:%s'%(response.url,response.status_code)
        return callback(response)


    def parse(self,response):
        """parse for response data"""

        #date = time.strftime('%Y%m%d%H%M',time.localtime(time.time()))
        auctions = response.json()['API.CustomizedApi']['itemlist']['auctions']
        items = [self.select_item(ac) for ac in auctions]
        return items


    def select_item(self,auction):
        """select item from auction"""

        fields = ('nid','category','raw_title','detail_url','view_price',
                  'view_fee','item_loc','view_sales','comment_count','user_id','nick','comment_url','shopLink')
        item = dict([(i,auction[i]) for i in fields])
        return item


    def grab_urls_from_items(self):
        return [i['comment_url'] for i in self.items]


    def save_data(self,conn):
        """save data in mysql"""

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


    def show_datas(self):
        """print datas"""

        items = self.items
        for i in items:
            print "%-15s %-50s %-10s %-10s %-100s" % (i['nick'], i['raw_title'], i['view_price'], i['view_sales'],i['comment_url'])


if __name__ == '__main__':
    pass











