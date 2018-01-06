# zxcs_spider
爬取知轩藏书的玄幻小说, 并用django展示

## 使用方法
* 初始化django数据库, 并使用爬虫积累数据
```python
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
cd zxcs_spider
python spider
```

* 积累数据完毕后, 使用django的后台功能查看数据结果
```python
cd ..
python manage.py runserver
浏览器输入 127.0.0.1/admin
进入 Novels 板块查看数据
```

## 爬虫特性
* 协程并发
* 可拓展代理
* 闭包requests, 完善requests功能
* 日志记录错误


## 进一步拓展
* 使用更多Djnago功能和JavaScript的逻辑
* 这个工作当然是由你来做

## 不要暴力爬取
* 知轩藏书是个好网站, 大家不要伤害他的服务器...一定要加延时