import requests
from lxml.html import fromstring
from logger import logger
import re
import gevent
import time
from queue import Queue
import inspect
try:
    from novels.models import Novels
except:
    import zxcs_spider.__init__
    from novels.models import Novels
from functools import wraps
# from proxies import get_a_proxy

url = 'http://www.zxcs8.com/sort/26'
url2 = 'http://www.zxcs8.com/content/plugins/cgz_xinqing/cgz_xinqing_action.php?action=show&id={}'
review = '仙草,粮草,干草,枯草,毒草'   # 评价分级
ua = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
s = requests.session()
re_queue = Queue()


def get_wrapper(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        def inner():
            try:
                logger.info('[开始爬取]' + args[0])
                r = fun(*args, **kwargs)
            except:
                logger.error('[出现异常]' + args[0] + '的爬取过程出现异常, 剩余重试次数' + str(retry), exc_info=True)
                r = ''
            return r
        retry = 3
        r = inner()
        while not r and retry > 0:
            r = inner()
            retry -= 1
        if r and r.status_code == 200:
            logger.info('[爬取成功]' + args[0])
        return r
    return wrapper

s.get = get_wrapper(s.get)


def parse_tree(tr):
    all_items = []
    all_pl = tr.xpath('//dl[@id="plist"]')
    for pl in all_pl:
        item = dict()
        dt = pl.xpath('dt')
        dd1 = pl.xpath('dd[@class="des"]')
        dd2 = pl.xpath('dd[not(@class)]')
        title = dt[0].xpath('a/text()')[0]
        code = dt[0].xpath('a/@href')[0].split('/')[-1]
        detail = dd1[0].text.strip()
        try:
            size, abstract = detail.split('【内容简介】')
            size = float(re.match('.*?(\d[.]\d+).*?', size).group(1))
        except:
            size, abstract = .0, detail
        else:
            abstract = '【内容简介】' + abstract.replace(r'\u3000\u3000', '')
        category = []
        all_cate = dd2[0].getchildren()
        for cate in all_cate:
            _ = cate.xpath('@href')
            if _ and 'author' not in _[0]:
                category.append(cate.text)
        item['title'] = title
        item['code'] = code
        item['size'] = size
        item['abstract'] = abstract
        item['category'] = ','.join(category)
        all_items.append(item)
    return all_items


def has_next(tr):
    next_node = tr.xpath('//div[@id="pagenavi"]/span/following-sibling::*[1]')
    if next_node and next_node[0].tag == 'a':
        logger.info('存在下一页')
        return next_node[0].xpath('@href')[0]
    return False


def get_review(code, item):
    logger.info('尝试获取' + item['title'] + '的评价数据')
    # text = s.get(url2.format(code), timeout=20, headers={'User-Agent': ua}, proxies=get_a_proxy()).text
    text = s.get(url2.format(code), timeout=20, headers={'User-Agent': ua}).text
    item['review'] = text
    logger.info(item['title'] + '  ' + text)
    logger.info('尝试保存到数据库')
    save_item(item)
    logger.info('保存数据库成功')


def save_item(item):
    if Novels.objects.filter(code=item['code']).exists():
        logger.info('已经存在' + item['title'] + ', 尝试更新数据')
        novel = Novels.objects.get(code=item['code'])
    else:
        novel = Novels()
    novel.title = item['title']
    novel.code = item['code']
    novel.category = item['category']
    novel.size = item['size']
    novel.abstract = item['abstract']
    novel.review = item.get('review', '')
    novel.save()


def main():
    urls = ['http://www.zxcs8.com/sort/26']
    while urls:
        u = urls.pop()
        logger.info('开始爬取列表页面: ' + str(u))
        # html = s.get(url, timeout=20, headers={'User-Agent': ua}, proxies=get_a_proxy()).text
        html = s.get(u, timeout=20, headers={'User-Agent': ua})
        if not html:
            continue
        html = html.text
        tree = fromstring(html)
        items = parse_tree(tree)
        g_list = []
        for item in items:
            code = item['code']
            ga = gevent.spawn(get_review, code, item)
            g_list.append(ga)
        gevent.joinall(g_list)
        n_url = has_next(tree)
        if n_url:
            time.sleep(5)
            urls.append(n_url)


if __name__ == '__main__':
    main()
