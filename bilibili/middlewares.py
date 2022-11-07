# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

class BilibiliSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BilibiliDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    cookies = {
        '_uuid': "BEC21480-9986-87AB-2A5E-61CBD3690F2263311infoc",
        'b_lsid': "BCB7B66C_180BBF1CC92",
        'b_ut': "5",
        'bili_jct': "f888ce48a77f8e8a84c270bcd40c60cf",
        'blackside_state': "0",
        'bp_video_offset_36676936': "659566260664664000",
        'bsource': "search_baidu",
        'buvid_fp': "fb529450ec7467883b6d304e7087f4b0",
        'buvid_fp_plain': "undefined",
        'buvid3': "E1CF8A9E-79B2-4273-8D42-8198B443E80B143108infoc",
        'buvid4': "C050A95B-8EE4-B525-2D4F-9F1ED0FC761945762-022012119-eD/hZZHkALBOJaP+S4SPTA==",
        'CURRENT_BLACKGAP': "0",
        'CURRENT_FNVAL': "4048",
        'CURRENT_QUALITY': "112",
        'DedeUserID': "36676936",
        'DedeUserID__ckMd5': "b15c224f76eb12c4",
        'dy_spec_agreed': "1",
        'fingerprint': "1820eceedbf7c9550239015a5f5b3064",
        'fingerprint_s': "bd1eb4aeb62b46f1e19a524455b85a3d",
        'fingerprint3': "dd6e9d3a8cc6fa171373fee010c47ff0",
        'hit-dyn-v2': "1",
        'i-wanna-go-back': "-1",
        'innersign': "1",
        'is-2022-channel': "1",
        'LIVE_BUVID': "AUTO5816047474799579",
        'LNG': "zh-CN",
        'nostalgia_conf': "-1",
        'PVID': "1",
        'rpdid': "|(k|)mku)Y0J'uY|Rl)kkJu",
        'SESSDATA': "88abc9f6,1665839745,8750f*41",
        'sid': "4rbu2be0",
        'video_page_version': "v_old_home",
    }
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        request.cookies = self.cookies
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
