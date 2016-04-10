import requests, re, os, bs4
from bs4 import BeautifulSoup as BSoup

import threading, queue

def multyThread(func):
    def thread(threadNum, queue):

        def loop():
            while True:
                argv = queue.get()
                succeed = False
                for i in range(5):
                    try:
                        func(*argv)
                        succeed = True
                        break
                    except StopIteration:
                        pass
                if not succeed:
                    print(func.__name__, argv, 'FAILED')
                    print('-'*80)
                queue.task_done()
        
        for i in range(threadNum):
            t = threading.Thread(target = loop)
            t.setDaemon(True)
            t.start()
            #func(*argv)

        queue.join()
        
    return thread

class Url:
    BASE_URL = 'http://book.easou.com/'
    def __init__(self, url):
        self.url = ''.join(re.match('(?:https?://)?(\S+)', url).groups())

    '''def connect(self, theUrl):
        a = self.url
        b = theUrl.url
        if (a[-1] == '/') ^ (b[0] == '/'):
            return a + b
        else:
            if b[0] == '/':
                return a + b[1:]
            else:
                return a + '/' + b'''

    def fullUrl(self, url):
        return self.connect(self.BASE_URL, url)
    
    def connect(a, b):
        if (a[-1] == '/') ^ (b[0] == '/'):
            return a + b
        else:
            if b[0] == '/':
                return a + b[1:]
            else:
                return a + '/' + b
            
    def __str__(self):
        return self.url

class WebPage:
    def __init__(self, url, encoding = 'utf-8', ip = None, timeout = 8):
        print(url)
        self.url = url
        self.page = requests.get(url)
        self.page.encoding = encoding
        self.html = self.page.text
        self.bsObj = BSoup(self.html, 'html.parser')

class ResourcePage(WebPage):
    def __init__(self, id_, resourceName = None, encoding = 'utf-8'):
        self.url = 'http://book.easou.com/w/sort/%s.html' % id_
        WebPage.__init__(self, self.url, encoding = encoding)
        reg = re.compile(r'最新章节\:[\s\S]*?更新日期：[\s\S]*?来源网址：\w*?')
        rBsObjs = filter(lambda x: re.findall(reg, x.text), self.bsObj.find_all('li'))
        self.resources = [
            (
                Url.fullUrl(Url, x.a.attrs.get('href')),
                #x.find('div', class_ = 'date').text,
                x.find('div', class_ = 'source').text[5:]
            )
            for x in rBsObjs
        ]
        #self.resources.sort(key = lambda x: x[1], reverse = True)
        
class IndexPage(WebPage):
    def __init__(self, url, encoding = 'utf-8'):
        categorePage = WebPage(url)
        self.desc = categorePage.bsObj.find('div', class_ = 'desc').text.strip()
        self.allCategoreUrl = categorePage.bsObj.find('div', class_ = 'allcategore').a.attrs.get('href')
        self.index = []
        
        categoreUrl = self.allCategoreUrl
        while categoreUrl:
            WebPage.__init__(self, Url.fullUrl(Url, categoreUrl), encoding = encoding)
            self.getIndex()
            categoreUrl = ([x.attrs['href'] for x in filter(lambda x: x.find('span', class_ = 'next'), self.bsObj.find_all('a', class_ = 'common'))] or [None])[0]
        
    def getIndex(self):
        aList = self.bsObj.find_all('a', class_ = 'common', text = re.compile(r'\d+\.[\s\S]+'))
        self.index += [(Url.fullUrl(Url, a.get('href')), a.text) for a in aList]

class ContentPage(WebPage):
    PAGE_RULE = {
        'sangwu.org': {
            'tag': 'div',
            'attr': {'class_': 'centent'},
            'coding': 'gbk'
        }, 
        'biquge.la': {
            'tag': 'div',
            'attr': {'id': 'content'},
            'coding': 'gbk'
        },
        'baquge.com': {
            'tag': 'div',
            'attr': {'class_': 'novel_content'},
            'coding': 'gbk'
        },
        'baishuku.com': {
            'tag': 'div',
            'attr': {'id': 'content'},
            'coding': 'gbk'
        },
        'ybdu.com': {
            'tag': 'div',
            'attr': {'id': 'htmlContent'},
            'coding': 'gbk'
        },
        'dajiadu.net': {
            'tag': 'div',
            'attr': {'id': 'content1'},
            'coding': 'gbk'
        },
        'biqiwu.com': {
            'tag': 'div',
            'attr': {'class_': 'content'},
            'coding': 'gbk'
        },
        '365if.com': {
            'tag': 'div',
            'attr': {'id': 'content'},
            'coding': 'gbk'
        },
        'xshuotxt.com': {
            'tag': 'div',
            'attr': {'id': 'content'},
            'coding': 'gbk'
        },
        'kiwang.com': {
            'tag': 'div',
            'attr': {'id': 'inner'},
            'coding': 'gbk'
        },
        'ttshuba.com': {
            'tag': 'div',
            'attr': {'id': 'TXT'},
            'coding': 'gbk'
        },
        'zaidudu.net': {
            'tag': 'dd',
            'attr':  {'id': 'contents'},
            'coding': 'gbk'
        },
        'mpzw.com': {
            'tag': 'div',
            'attr': {'id': 'clickeye_content'},
            'coding': 'gbk'
        },
        'yssm.org': {
            'tag': 'div',
            'attr': {'id': 'content'},
            'coding': 'utf-8'
        },
        'yjxs.net': {
            'tag': 'dd',
            'attr': {'id': 'contents'},
            'coding': 'gbk'
        },
        'klxsw.com': {
            'tag': 'div',
            'attr': {'id': 'r1c'},
            'coding': 'gbk'
        },
        'aszw.com': {
            'tag': 'div',
            'attr': {'id': 'contents'},
            'coding': 'gbk'
        }
    }

    DEFAULT_RULE = {
        'tag': 'div',
        'attr': {'id': 'content'},
        'coding': 'gbk'
    }
    
    def __init__(self, url, site):
        RULE = self.PAGE_RULE.get(site, self.DEFAULT_RULE)
        for tolerance in range(10):
            WebPage.__init__(self, url, encoding = RULE['coding'])
            if len(self.html) > 2000:
                break
            print('Jumping..')
            url = Url.connect('http://www.' + site, re.search('location\s*=\s*"(\S+?.html)', self.html).groups()[0])
            print(url)
            
        self.contentBs = self.bsObj.find(RULE['tag'], **RULE['attr']).contents
        self.content = [c.strip() for c in filter(lambda x: isinstance(x, bs4.element.NavigableString) and x.strip(), self.contentBs)]

class Chapter:
    def __init__(self, site, url, title, watch = True):
        self.site = site
        self.url = url
        self.titleInfo = self.analyzeTitle(title)
        for i in self.titleInfo:
            if not self.titleInfo[i]:
                self.titleInfo[i] = ''
        self.content = ContentPage(self.url, self.site).content

        if watch:
            print(title)
            for c in self.content:
                print(' ' * 4 + c)

    @staticmethod
    def analyzeTitle(title):
        print(title)
        titleRule = re.compile(r'((?P<chapter_id>\d+?)\.)?[\s\S]*?(?:(?P<part_order>第[零〇一二两三四五六七八九十百千万零壹贰叁肆伍陆柒捌玖拾佰仟万\d]+[卷章节回]?)\s*(?P<part_name>\S+?\s*))??(?:(?P<chapter_order>第[零〇一二两三四五六七八九十百千万零壹贰叁肆伍陆柒捌玖拾佰仟万\d]+[卷章节回]?)\s*)?(?P<chapter_title>\S+?)\s*$')
        res = re.match(titleRule, title).groupdict()
        return res

class Novel:
    def __init__(self, id_, resource = ""):
        self.id = id_
        self.getResourceDetail(resource)
        self.site, self.index = self.res[0]            
        self.chapterNum = len(self.index)
        
        '''for r in self.res:
            self.site, self.index = r#self.res[0]
            #self.index = IndexPage(self.resUrl).index
            #latest now, do that later
            print("'%s': {\n'tag': \n'attr':\n'coding': 'gbk'\n}," % self.site)
            try:
                self.chapter = Chapter(self.site, *self.index[-1]) #TODO:
            except:
                print(self.site, 'FAILED.')'''

    def getResourceDetail(self, resource = ""):
        resources = ResourcePage(self.id).resources
        resourceFilter = list(filter(lambda x: x[1] == resource, resources))
        if not resourceFilter:
            resourceFilter = resources
        self.desc = ''
        self.res = []
        print(resourceFilter)
        q = queue.Queue()

        @multyThread
        def analyse(x):
            i = IndexPage(x[0])
            print(x[1])
            if not self.desc:
                self.desc = ''.join(
                    [
                        '<span style = "opacity: 0;">____</span>' + x + '<br />'
                        for x in
                        filter(lambda x: x, re.split(r'\s', i.desc))
                    ]
                )
            self.res += [(x[1], i.index)]
        
        for x in resourceFilter: 
            q.put((x, ))
            
        analyse(100, q)
            
        self.res.sort(key = lambda x: -len(x[1]))
        return self.res
        

    def getChapter(self, chapterOrder, watch = True):
        print(chapterOrder)

        succeed = False
        for i in range(5):
            try:
                chapter = Chapter(self.site, *self.index[chapterOrder], watch)
                chapter.order = chapterOrder % self.chapterNum + 1
                succeed = True
                break
            except:
                pass
        if not succeed:
            print('FAILED')
            return None
        return chapter

@multyThread
def go(a, b, c):
    print(a, b, c)
        
if __name__ == "__main__":
    #novel = Novel('18403861')
    novel = Novel('8783053', 'biquge.la')
    '''q = queue.Queue()

    for i in range(1):
        q.put((i, i + 1, i + 2))
        
    go(300, q)

'''
