# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from uniqlo.spiders import utils
from uniqlo.settings import *
import json


class UniqloPipeline:

    def __init__(self):
        self.db = utils.set_mongo_server()

    def process_item(self, item, spider):
        try:
            if 'name' in item:
                self.db[MONGODB_COLNAME].insert(dict(item))
        except Exception as ex:
            self.logger.warn('Pipeline Error (others): %s  %s' %(str(ex), str(item)))
        return item
