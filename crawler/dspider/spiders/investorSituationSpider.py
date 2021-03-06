# -*- coding: utf-8 -*-
import re
import datetime
from datetime import datetime
from scrapy import FormRequest
from dspider.utils import datetime_to_str
from dspider.myspider import BasicSpider
from dspider.items import InvestorSituationItem
investor_count_to_path = {
    "date"                    :"/html/body/div/h2/text()",#日期
    "new_investor"            :"//*[@id='settlementList']/table/tbody/tr/td/table/tbody/tr[2]/td[2]/p/span/text()", #新增投资者数量
    "final_investor"          :"//*[@id='settlementList']/table/tbody/tr/td/table/tbody/tr[5]/td[2]/p/span/text()", #期末投资者数量
    "new_natural_person"      :"//*[@id='settlementList']/table/tbody/tr/td/table/tbody/tr[3]/td[2]/p/span/text()", #新增投资者中自然人数量
    "new_non_natural_person"  :"//*[@id='settlementList']/table/tbody/tr/td/table/tbody/tr[4]/td[2]/p/span/text()", #新境投资者中非自然人数量
    "final_natural_person"    :"//*[@id='settlementList']/table/tbody/tr/td/table/tbody/tr[6]/td[2]/p/span/text()", #期末投资者中自然人数量
    "final_non_natural_person":"//*[@id='settlementList']/table/tbody/tr/td/table/tbody/tr[10]/td[2]/p/span/text()",#期末投资都中非自然人数量
    "unit"                    :"//*[@id='settlementList']/table/tbody/tr/td/table/tbody/tr[1]/td[2]/p/strong/span/text()"#单位
}

class InvestorSituationSpider(BasicSpider):
    name = 'investorSituationSpider'
    custom_settings = {
        'ITEM_PIPELINES': {
            'dspider.pipelines.DspiderPipeline': 2
        }
    }
    allowed_domains = ['www.chinaclear.cn']
    start_urls = ['http://www.chinaclear.cn/cms-search/view.action']
    def start_requests(self):
        formdata = dict()
        formdata['dateType'] = ''
        formdata['channelIdStr'] = '6ac54ce22db4474abc234d6edbe53ae7'
        end_date = datetime.now().strftime('%Y.%m.%d')
        start_date = self.get_nday_ago(end_date, 60, dformat = '%Y.%m.%d')
        while start_date < end_date:
            start_date = self.get_next_date(sdate = start_date)
            formdata['dateStr'] = start_date
            yield FormRequest(url = self.start_urls[0], method = 'GET', formdata = formdata, callback = self.parse)

    def parse(self, response):
        patten = re.compile(r'[（](.*?)[）]', re.S)
        investor_situation_item = InvestorSituationItem()
        for k in investor_count_to_path:
            if k == "date":
                tmpstr = response.xpath(investor_count_to_path[k]).extract_first()
                if tmpstr == '搜索结果': return
                mdate = re.findall(patten, tmpstr)[0].split('-')[1].strip()
                mdate = mdate.replace('.', '-')
                investor_situation_item[k] = mdate 
            else:
                investor_situation_item[k] = response.xpath(investor_count_to_path[k]).extract_first().strip()
        yield investor_situation_item
