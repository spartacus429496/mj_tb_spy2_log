# -*- coding: utf-8 -*-

from scrapy.dupefilters import RFPDupeFilter

class SeenURLFilter(RFPDupeFilter):
    def request_seen(self, request):
        return False # 不做重复检查