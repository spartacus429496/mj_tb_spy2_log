# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class __shop_commodity():
    shop_number=0
    commodity_name=""
    commodity_id=0
    commodity_url=""
    commodity_price=0
    commodity_promo_price=0
    commodity_sales=0
    commodity_stock=0
    commodity_comment=0

class TaobaoShop(Item):
# common filed
    shop_number = Field()
    shop_seller_id = Field()
    shop_classify = Field()
    shop_reserver = Field()
    shop_name = Field()
    shop_owner = Field()
    shop_url = Field()
    shop_detail_url = Field()
    shop_location = Field()
    shop_trade_range = Field()
    # shop_commodity = __shop_commodity()

# tmall    
    shop_commany_name = Field()
    shop_telephone = Field()
# taobao
    shop_create_time = Field()
    shop_popularity = Field()
    shop_credit = Field()