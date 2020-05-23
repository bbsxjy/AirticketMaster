# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
from collections import OrderedDict
from scrapy import signals
from time import strftime


class AirticketmasterPipeline(object):

    def __init__(self):
        currentTime = strftime("%m%d%H%M");
        filePath = "./AirticketMaster/data/" + str(currentTime) + ".json"

        self.file = codecs.open(filePath, 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()