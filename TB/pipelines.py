# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# import MySQLdb

class TbPipeline(object):
    def process_item(self, item, spider):
        return item
'''
    def open_spider(self, spider):
        self.sqlconn = MySQLdb.connect(host='localhost',
                                       port = 3306,
                                       user='root',
                                       passwd='123456',
                                       db ='mj_test')
        self.sqlcur = self.sqlconn.cursor()

    def close_spider(self, spider):
        self.sqlcur.close()
        self.sqlconn.close()
'''