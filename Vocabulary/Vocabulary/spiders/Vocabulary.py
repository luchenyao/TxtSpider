# coding=utf=8
# Author: LuChenyao
# Date:2018-03-26


import scrapy


class VocItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()


class LawSpider(scrapy.Spider):
    name = 'vocabulary'
    start_urls = ["http://baike.baidu.com/"]

    def start_requests(self):
        urls = [
            'http://baike.baidu.com/fenlei/%E6%B3%95%E5%BE%8B',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        category = response.xpath('//div[@class="category-title "]')
        if category:
            # 如果是词条列表， 则将词条、分类的翻页、子分类加入队列
            """当前分类下的词条加入队列"""
            item_list = response.xpath('//div[@class="grid-list grid-list-spot"]//div[@class="list"]/a/@href').extract()
            for item_url in item_list:
                if '/view/' in item_url:
                    yield scrapy.Request('http://baike.baidu.com' + item_url, callback=self.parse)

            ############################################
            # 这段内容调试单个页面的时候建议注释关掉
            # Begin

            """当前分类的翻页加入队列"""
            indexs = response.xpath('//div[@id="pageIndex"]/a/@href').extract()
            for url in indexs:
                yield scrapy.Request('http://baike.baidu.com/fenlei/' + url, callback=self.parse)

            """将子分类的url加入队列"""
            sub_urls = category.xpath('./a/@href').extract()
            for url in sub_urls:
                yield scrapy.Request('http://baike.baidu.com' + url, callback=self.parse)
                # End
                ############################################

        else:
            # 如果是词条，处理词条内容，抓取需要的内容
            ############################################
            """TODO"""
            titles=response.xpath('//div[@class="content"]//dd[@class="lemmaWgt-lemmaTitle-title"]/h1//text()').extract()
            for each in titles:
                title=''.join(each).strip()
            con_str=response.xpath('//div[@class="lemma-summary"]//div[@class="para"]//text()').extract()
            contents = ''.join(con_str)
            contents = contents.strip()
            if contents:
                con_str2 = response.xpath('//div[@class="main-content"]/div[@class="para"]//text()').extract()
                content=''.join(con_str2)
                content=content.strip()
                contents=contents+content
                contents.replace(u'\n', '')  # 换行符
                contents.replace(u'\r', '')  # 回车符
                contents.replace(u'\t', '')  # 水平制表符
                contents.replace(u' ', '')  # 空格符
                contents=contents.strip()

            else:
                con_str=response.xpath('//div[@class="lemma-summary"]//text()').extract()
                contents = ''.join(con_str)
                contents=contents.strip()
                con_str2 = response.xpath('//div[@class="main-content"]/div[@class="para"]//text()').extract()
                content = ''.join(con_str2)
                content=content.strip()
                contents = contents + content
                contents.replace(u'\0x000A', '')  # 换行符
                contents.replace(u'\0x000D', '')  # 回车符
                contents.replace(u'\0x0009', '')  # 水平制表符
                contents.replace(u'\0xA1A1', '')  # 空格符
                contents = contents.strip()

            yield VocItem(title=title,content=contents)

            pass
