# -*- coding: utf-8 -*-

import re
import json
import scrapy
import string
import HTMLParser
import time

from TB.items import TaobaoShop

class TaobaoSpider(scrapy.spiders.Spider):
    """docstring for taobao_spider"""
    name = "tb_spider"

    # current_shopid = 67482531
    current_shopid = 67482751
    # current_shopid = 67485766
    # start_urls = ["http://192.168.171.3:80"]
    start_urls = ["https://shop67482751.taobao.com"]

    def __init__(self):
        self.pre_login_fill_info()
        print self.start_urls[0]

    def pre_login_fill_info(self):
        #登录的URL
        self.loginURL = "https://login.taobao.com/member/login.jhtml"
        #用户名
        self.username = '15715513873'
        #ua字符串，经过淘宝ua算法计算得出，包含了时间戳,浏览器,屏幕分辨率,随机数,鼠标移动,鼠标点击,其实还有键盘输入记录,鼠标移动的记录、点击的记录等等的信息
        self.ua = '103UW5TcyMNYQwiAiwTR3tCf0J/QnhEcUpkMmQ=|Um5OcktyTXhFfURxSXJPcyU=|U2xMHDJ+H2QJZwBxX39RaFV7W3UpSC5CJVshD1kP|VGhXd1llXGVab1JqU2ZeYFRoX2JAe056RnNJdU9yTnBNcEt1SWcx|VWldfS0QMAswEC4OIBQxByl/KQ==|VmNDbUMV|V2NDbUMV|WGRYeCgGZhtmH2VScVI2UT5fORtmD2gCawwuRSJHZAFsCWMOdVYyVTpbPR99HWAFYVMoRSlIM141SBZPCTlZJFkgCTYOMHtSbVVqJg8wCDd7EW0dcAspVC9GKkdlGHEWfBVyUDtcORAvFyhkGWILZwojHCQbVzZLJkMnRjxBaFdvUBx4GWMeSiBHO1Q0SR18AWwJc1ExTCkHJwkncSc=|WWdHFy0RMQwsECkWKAg9CTcXKxIrFjYCPwIiHiceIwM2DDFnMQ==|WmBAED4QMAwsFyl/KQ==|W2FBET8RMQwsFC4UK30r|XGVFFTtkP3ktVD1HPUMkXzNnW3VVaVRpVXVKf0pqVGhVYFUDVQ==|XWVFFTsVNWVfZ1NzTHdKHDwBIQ8hAT8AOw4xZzE=|XmREFDoUNAgoFikSJhhOGA==|X2dHFzl5LXUJYwZnGkI/VitKIQ8vf0t+Q2NdaFwKKhc3GTcXKREkESVzJQ==|QHpaCiRkMGgUfht6B18iSzZXPBIyDi4QKB0pEkQS|QXhFeFhlRXpaZl9jQ31Ff19nU3NJcVFtUWhIdFRtUHBOelpiQn5AYF5lRXlFZVtiNA=='
        #密码，在这里不能输入真实密码，淘宝对此密码进行了加密处理，256位，此处为加密后的密码
        self.password2 = '7dec75624edf5765b68b8e50e3cfda68b93ac0b20eca0567ba8126ac960799b3701a8fe81d51e73c8916890452fd41932428d84796053872df37e1398dd3e2dbaa5f178ec25e63330effeace4f6b38170afdc5cd69f7436a02afc26ebf7222060ea09424daea8bab9c1e9c84f3491ccc84ee72228ea250f8b93508c40fd70831'
        self.loginPOST = {
            'ua':self.ua,
            'TPL_username':self.username,
            'TPL_password':'',
            'TPL_checkcode':'',
            'CtrlVersion': '1,0,0,7',
            'TPL_redirect_url':'',
            'loginsite':'0',
            'newlogin':'0',
            'from':'tb',
            'fc':'default',
            'style':'default',
            'css_style':'',
            'tid':'',
            'support':'000001',
            'loginType':'4',
            'minititle':'',
            'minipara':'',
            'umto':'NaN',
            'pstrong':'3',
            'llnick':'',
            'sign':'',
            'need_sign':'',
            'isIgnore':'',
            'full_redirect':'',
            'popid':'',
            'callback':'',
            'guf':'',
            'not_duplite_str':'',
            'need_user_id':'',
            'poy':'',
            'gvfdcname':'10',
            'gvfdcre':'',
            'from_encoding ':'',
            'sub':'',
            'TPL_password_2':self.password2,
            'loginASR':'1',
            'loginASRSuc':'1',
            'allp':'',
            'oslanguage':'zh-CN',
            'sr':'1366*768',
            'osVer':'windows|6.1',
            'naviVer':'firefox|35'
        }

    def __next_task_url(self):
        url = "https://shop%ld.taobao.com" % self.current_shopid
        self.current_shopid += 1
        print "下一个店铺的地址 %s" % url
        return url

    def __decode_tb_json(self, data, charset):
        json_set = set()

        start = data.find("(")
        end =   data.rfind(")")
        if start < 0 or end < 0:
            print "无法识别json文件"
        else:
            try:
                data = unicode(data[start+1:end], charset)
            except:
                print "json 字符集错误"
            else:
                htmlparser = HTMLParser.HTMLParser()
                json_set = json.loads(data)
        return json_set

    def parse(self, response):
        # print response.body
        # yield scrapy.FormRequest(url=self.loginURL, formdata=self.loginPOST, callback=self.needCheckCode)
        yield scrapy.Request(self.__next_task_url(), callback=self.tb_parse)        
    
    #得到是否需要输入验证码，这次请求的相应有时会不同，有时需要验证有时不需要
    def needCheckCode(self, response):
        # #第一次登录获取验证码尝试，构建request
        # request = urllib2.Request(self.loginURL,self.postData,self.loginHeaders)
        # #得到第一次登录尝试的相应
        # response = self.opener.open(request)
        # #获取其中的内容
        # content = response.read().decode('gbk')
        content = unicode(response.body, "gbk")

        #状态码为200，获取成功
        if response.status == 200:
            print u"获取请求成功"
            #\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801这六个字是请输入验证码的utf-8编码
            # pattern = re.compile(u'\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801',re.S)
            pattern = re.compile(u'输入验证码', re.S)
            result = re.search(pattern,content)
            #如果找到该字符，代表需要输入验证码
            if result:
                print u"此次安全验证异常，您需要输入验证码"
                #得到验证码的图片
                pattern = re.compile('<img id="J_StandardCode_m.*?data-src="(.*?)"',re.S)

                #匹配的结果
                matchResult = re.search(pattern,response.body)

                #已经匹配得到内容，并且验证码图片链接不为空
                if matchResult and matchResult.group(1):
                    # checkcode_url = matchResult.group(1)
                    # print "%s" % checkcode_url
                    # checkcode = raw_input('请输入验证码:')

                    # self.loginPOST['TPL_checkcode'] = checkcode
                    # self.loginPOST['loginType'] = '4'
                    # yield scrapy.FormRequest(url=self.loginURL, 
                    #                          formdata=self.loginPOST, 
                    #                          callback=self.loginWithCheckCode)
                    time.sleep(1)
                    yield scrapy.FormRequest(url=self.loginURL, formdata=self.loginPOST, callback=self.needCheckCode)

                else:
                    print u"没有找到验证码内容"
                    return
            #否则不需要
            else:
                #返回结果直接带有J_HToken字样，表明直接验证通过
                tokenPattern = re.compile('id="J_HToken" value="(.*?)"')
                tokenMatch = re.search(tokenPattern,content)
                if tokenMatch:
                    J_HToken = tokenMatch.group(1)
                    print u"此次安全验证通过，您这次不需要输入验证码"
                    yield scrapy.Request(url="https://passport.alipay.com/mini_apply_st.js?site=0&token=%s&callback=stCallback6" % J_HToken,
                                        callback=self.getSTbyToken)
        else:
            print u"获取请求失败"
            return

    def getSTbyToken(self,response):
        # tokenURL = 'https://passport.alipay.com/mini_apply_st.js?site=0&token=%s&callback=stCallback6' % token
        # request = urllib2.Request(tokenURL)
        # response = urllib2.urlopen(request)
        #处理st，获得用户淘宝主页的登录地址
        pattern = re.compile('{"st":"(.*?)"}',re.S)
        result = re.search(pattern,response.body)
        #如果成功匹配
        if result:
            print u"成功获取st码"
            #获取st的值
            st = result.group(1)
            # return st
            yield scrapy.Request(url='https://login.taobao.com/member/vst.htm?st=%s&TPL_username=%s' % (st,self.username),
                                callback=self.loginByST)
        else:
            print u"未匹配到st"
            return

    #利用st码进行登录,获取重定向网址
    def loginByST(self, response):
        # stURL = 'https://login.taobao.com/member/vst.htm?st=%s&TPL_username=%s' % (st,username)
        # headers = {
        #     'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
        #     'Host':'login.taobao.com',
        #     'Connection' : 'Keep-Alive'
        # }
        # request = urllib2.Request(stURL,headers = headers)
        # response = self.newOpener.open(request)

        content =  unicode(response.body, "gbk")

        #检测结果，看是否登录成功
        pattern = re.compile('top.location = "(.*?)"',re.S)
        match = re.search(pattern,content)
        if match:
            print u"登录网址成功"
            location = match.group(1)
            yield scrapy.Request(self.__next_task_url(), callback=self.tb_parse)

        else:
            print "登录失败"
            return

    #输入验证码，重新请求，如果验证成功，则返回J_HToken
    def loginWithCheckCode(self, response):
        #获取其中的内容
        content = unicode(response.body, "gbk")
        pattern = re.compile(u'验证码错误', re.S)
        result = re.search(pattern,content)

        #如果返回页面包括了，验证码错误五个字
        if result:
            print u"验证码输入错误"
            return
        else:
            #返回结果直接带有J_HToken字样，说明验证码输入成功，成功跳转到了获取HToken的界面
            tokenPattern = re.compile('id="J_HToken" value="(.*?)"')
            tokenMatch = re.search(tokenPattern,content)
            #如果匹配成功，找到了J_HToken
            if tokenMatch:
                print u"验证码输入正确"
                J_HToken = tokenMatch.group(1)
                yield scrapy.Request(url="https://passport.alipay.com/mini_apply_st.js?site=0&token=%s&callback=stCallback6" % J_HToken,
                                    callback=self.getSTbyToken)
            else:
                #匹配失败，J_Token获取失败
                print u"J_Token获取失败"
                return

    def tb_parse(self, response):
        resp_url = response.url
        if ("noshop.htm" in resp_url) or ("error1.html" in resp_url):
            # 当前url无效， 获取下一个任务
            print '店铺不存在'

        yield scrapy.Request(self.__next_task_url(), callback=self.tb_parse)
        '''
            t = response.xpath('//title/text()').extract()

            print "解析店铺主页面 %s" % resp_url
 
            self.shop = TaobaoShop(shop_number=self.current_shopid,
                                   shop_url=resp_url, 
                                   shop_name="",
                                   shop_owner="",
                                   shop_detail_url="",
                                   shop_location="",
                                   shop_trade_range="",
                                   shop_create_time="", 
                                   shop_popularity=0,
                                   shop_credit=0,
                                   shop_commany_name="", 
                                   shop_telephone="")

            if len(t) == 0:
                print "解析主页面错误"
                yield scrapy.Request(self.__next_task_url(), callback=self.tb_parse)
            else:
                if  t[0].find(u"Tmall.com") >= 0:
                    self.shop['shop_classify'] = 1
                    n = response.xpath("//a[@class='slogo-shopname']//text()").extract()
                    l = response.xpath("//*[@id='dsr-ratelink']/@value").extract()

                    if len(n) == 0 or len(l) == 0:
                        print "解析天猫店铺基本信息错误"
                        yield scrapy.Request(self.__next_task_url(), callback=self.tb_parse)
                    else:
                        self.shop['shop_name'] = n[0]
                        self.shop['shop_detail_url'] = "https:" + l[0]
                        yield scrapy.Request(self.shop['shop_detail_url'], callback=self.parse_tmall_detail)
                else:
                    l = response.xpath('//span[@class="shop-rank"]//a/@href').extract()
                    if len(l) != 1:
                        yield scrapy.Request(self.__next_task_url(), callback=self.tb_parse)
                    else:
                        url = "https:"+l[0]

                        self.shop['shop_classify'] = 0
                        self.shop['shop_detail_url'] = url

                        shop_name = response.xpath("//a[@class='shop-name']//text()").extract()
                        if len(shop_name) != 0:
                            self.shop["shop_name"] = shop_name[0]

                        yield scrapy.Request(url, callback=self.parse_tbshop_detail)
        '''

    def parse_tbshop_detail(self, response):
        print "解析店铺详细信息 %s" % response.url

        if "anti_Spider" in response.url:
            print "Oohs!"

        htmlparser = HTMLParser.HTMLParser()

        # 解析好评率
        rate  = response.xpath("//*[@class='tb-rate-ico-bg ico-seller']/em/text()").extract()
        if len(rate) != 0:
            rate = rate[0].split(u"：")
            if len(rate) == 2:
                try:
                    rate = string.atof(rate[1][:-1])
                except:
                    print "malform string: %s" % rate
                else:
                    self.shop["shop_credit"] = rate
        else:
            print "解析好评率错误"

        # 解析建店时间
        startdate = response.xpath("//input[@id='J_showShopStartDate']/@value").extract()
        if len(startdate) == 1:
            self.shop["shop_create_time"] = startdate[0]
        else:
            print "解析建店时间错误"


        # 解析店主名称
        owner = response.xpath("//div[@class='title']/a/text()").extract()
        if  len(owner) != 0:
            self.shop["shop_owner"] = owner[0]
        else:
            print "解析店主名称错误"

        # 解析当前主营
        trade_key = u"当前主营".encode("gbk")
        # 解析所在地区
        location_key = u"所在地区".encode("gbk")

        elements = re.findall("<li>(.*)</li>", response.body)
        for el in elements:
            if el.find(trade_key) >=0:
                el = re.findall("<a href=\".*\">(.*)</a>", unicode(el, "gbk"))
                if len(el) == 1:
                    el = htmlparser.unescape(el[0]) # 去掉HTML的转义字符
                    self.shop["shop_trade_range"] = el
                else:
                    print "解析当前主营错误"

            elif el.find(location_key) >= 0:
                el = unicode(el, "gbk").split(u"：")
                if len(el) == 2:
                    self.shop["shop_location"] = htmlparser.unescape(el[1]).strip()
                else:
                    print "解析所在地区错误"
                break;

        # 解析卖家信用
        credit_key = u"卖家信用：".encode("gbk")
        start = response.body.find(credit_key)
        if start >= 0:
            start += len(credit_key)
            end = start
            while 1:
                if response.body[end] == '\r':
                    break
                end += 1
            try:
                credit = string.atoi(response.body[start:end].strip())
                self.shop["shop_credit"] = credit
            except:
                print "解析信用错误"

        if self.shop["shop_location"] == "":
            # 如果在前面没有解析出地址(可能是店家没有写),
            # 就从这家店铺商品的收货地址取得其店铺地址
            url = "https://list.taobao.com/itemlist/default.htm?nick=%s&_input_charset=utf-8&json=on&callback=jsonp161" \
                   % self.shop['shop_owner'].encode("utf8")
            yield scrapy.Request(url, callback=self.parse_location_by_shipping_addr)
        else:
            print self.shop["shop_location"]
            if self.shop["shop_location"].find(u"合肥") < 0:
                yield scrapy.Request(self.__next_task_url(), callback=self.tb_parse)
            else:
                # url = "https://list.taobao.com/itemlist/default.htm?nick=%s&style=list&_input_charset=utf-8&json=on&callback=jsonp731" \
                #        % self.shop['shop_owner'].encode("utf8")
                yield scrapy.Request(url, callback=self.parse_commodity)
                # yield scrapy.Request(self.__next_task_url(), callback=self.tb_parse)
                yield self.shop

    def parse_tmall_detail(self, response):
        print "解析天猫店铺详细信息 %s" % response.url

        # 解析店主名称
        owner = response.xpath("//div[@class='title']/a/text()").extract()
        if  len(owner) != 0:
            self.shop["shop_owner"] = owner[0]
        else:
            print "解析店主名称错误"

        ul = response.xpath("//li[@class='company']/..") 
        if len(ul) != 1:
            print "解析天猫店铺详细信息错误"
        else:
            company_name = ul.xpath("..//div[@class='fleft2']/text()").extract()

            if len(company_name) == 0:
                print "解析天猫店铺公司名称错误"
            else:
                self.shop["shop_commany_name"] = company_name[0]

            trade = ul.xpath("..//li/a/text()").extract()
            if len(trade) == 0:
                print "解析天猫店铺主营范围错误"
            else:
                self.shop["shop_trade_range"] = trade[0].strip()

            li = ul.xpath("li")
            for i in li:
                loc = i.xpath("text()").extract()
                if len(loc) == 1:
                    loc = loc[0].split(u"：")
                    if len(loc) == 2 and loc[0].find(u"所在地区") >= 0:
                        self.shop["shop_location"] = loc[1]
                        break


            if self.shop["shop_location"] == "":
                # 如果在前面没有解析出地址(可能是店家没有写)，
                # 就从这家店铺商品的收货地址取得其店铺地址
                yield scrapy.Request(self.__next_task_url(), callback=self.tb_parse)
            else:
                print self.shop["shop_location"]

                if self.shop["shop_location"].find(u"合肥") < 0:
                    yield scrapy.Request(self.__next_task_url(), callback=self.tb_parse)
                else:
                    # url = "https://list.taobao.com/itemlist/default.htm?nick=%s&style=list&_input_charset=utf-8&json=on&callback=jsonp731" \
                    #        % self.shop['shop_owner'].encode("utf8")
                    # yield scrapy.Request(url, callback=self.parse_commodity)
                    yield scrapy.Request(self.__next_task_url(), callback=self.tb_parse)
                    yield self.shop

    # 通过店铺商品的收货地址来得到店铺地址
    def parse_location_by_shipping_addr(self, response):
        resp_url = response.url
        if "anti_Spider" in resp_url:
            print "Oohs ！！！遭遇反爬虫"
            yield scrapy.Request(self.__next_task_url(), callback=self.tb_parse)
        else:
            json_set = self.__decode_tb_json(response.body, "gbk")
            if "itemList" in json_set:
                itemlist = json_set['itemList']
                print "==========================="
                if itemlist != None and len(itemlist) != 0:
                    self.shop['shop_location'] = itemlist[0]['loc'].strip()
                    print self.shop['shop_location']

            yield scrapy.Request(self.__next_task_url(), callback=self.tb_parse)

    def parse_commodity(self, response):
        print response.body
        return

