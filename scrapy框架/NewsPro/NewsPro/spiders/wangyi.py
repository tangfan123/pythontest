import scrapy
from scrapy.http import Request
from ..items import NewsproItem


class WangyiSpider(scrapy.Spider):
    name = "wangyi"
    # allowed_domains = ["news.163.com"]
    start_urls = ["https://news.163.com/"]

    cate_list = []  # 每一个板块对应的url

    cate_num_map = {
        "{{__i == 0}}": "要闻",
        "{{__i == 1}}": "广州",
        "{{__i == 2}}": "国内",
        "{{__i == 3}}": "国际",
    }

    def parse(self, response):
        # with open("new163.html", "w", encoding="utf-8") as f:
        #     f.write(response.text)

        cate_list = response.xpath('//div[contains(@ne-if,"{{")]/@ne-if').extract()  # 拿到所有悬浮标签的属性
        for cate_num in cate_list:
            if cate_num in self.cate_num_map:  # 如果{{__i == 0}}在映射map里面就进行进一步解析拿到每条新闻的链接和内容名
                cate_title = self.cate_num_map.get(cate_num)
                news_list = response.xpath(f'//*[contains(@ne-if,"{cate_num}")]/div/a')  # 所有新闻的a标签

                for news_selecor in news_list:  # 解析所有A标签拿到链接和内容名字
                    news_title = news_selecor.xpath('text()').extract_first()  # 新闻内容标题
                    news_href = news_selecor.xpath('@href').extract_first()  # 链接

                    # 对新闻详情页的url发起请求
                    # 这里的yield表示还有url需要回调，示例流程图片第8步骤
                    # callback回调函数，还有请求处理需要回调函数
                    yield Request(url=news_href, callback=self.parse_news_calback, meta={
                        "cate_title": cate_title,
                        "news_title": news_title,
                    })

    # 回调函数
    def parse_news_calback(self, response):
        cate_title = response.meta.get("cate_title")
        news_title = response.meta.get("news_title")
        # 解析新闻内容
        # //div[@class="post_body"]/p
        news_content = response.xpath('//div[@class="post_body"]/p/text()').extract()
        news_content = ''.join([i.strip() for i in news_content])
        print("cate_title::", cate_title)  # 悬浮标题
        print("news_title::", news_title)  # 新闻内容标题
        print("news_content::", news_content)  # 新闻内容

        newItem = NewsproItem()
        newItem["cate_title"] = cate_title
        newItem["news_title"] = news_title
        newItem["news_content"] = news_content

        yield newItem
