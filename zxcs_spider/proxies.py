from redis import Redis
from queue import Queue
from logger import logger
import config


def load_settings(s):
    di = vars(s)
    se = dict()
    for k, v in di.items():
        if not k.startswith('__'):
            se[k] = v
    return se


def load_proxies():
    global proxies_queue
    usable_proxies = redis_conn.smembers('good_proxies')
    for i in usable_proxies:
        proxies_queue.put_nowait(i)


def get_a_proxy():
    global proxies_queue
    if proxies_queue.qsize() < 10:
        load_proxies()
    pr = proxies_queue.get().decode('utf-8')
    logger.info('获得代理' + pr)
    return {'http': '{}'.format(pr)}


settings = load_settings(config)
proxies_queue = Queue()
logger.info('连接远程redis服务器'+settings['REDIS_HOST']+':'+settings['REDIS_PORT']+':'+str(settings['REDIS_DB']))
redis_conn = Redis(settings['REDIS_HOST'], settings['REDIS_PORT'], settings['REDIS_DB'])
logger.info('远程redis服务器连接成功')