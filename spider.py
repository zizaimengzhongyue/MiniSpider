#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib.request
import re
import queue
import time

class Spider:

    def __init__(self, list_entry, list_path_rules, list_data_rules):
        self.list_entry = list_entry
        self.list_path_rules = list_path_rules
        self.list_data_rules = list_data_rules

    def _output(self, data):
        obj_ch = open("ip_list.txt", "a")
        for str_item in data:
            obj_ch.write(str_item + '\n')
        obj_ch.close()

    def _uniq(self, list_data):
        list_new_data = []
        dic_keys = {}
        for str_item in list_data:
            if str_item in dic_keys:
                continue
            dic_keys[str_item] = True
            list_new_data.append(str_item)
        return list_new_data

    def run(self):
        obj_queue = queue.Queue()
        for str_item in self.list_entry:
            obj_queue.put(str_item)
        list_ans = []
        dic_url = {}
        int_step = 1
        while not obj_queue.empty():
            str_url = obj_queue.get()
            print("第 " + str(int_step) + " 次抓取，url: " + str_url)
            int_step = int_step + 1
            obj_ch = urllib.request.urlopen(str_url)
            # 抓取数据
            str_content = obj_ch.read().decode('utf-8')
            for str_item in self.list_data_rules:
                list_matches = re.findall(str_item, str_content)
                list_ans = list_ans + list_matches
            # 抓取 url
            for str_item in self.list_path_rules:
                list_matches = re.findall(str_item, str_content)
                for str_url in list_matches:
                    if not str_url in dic_url:
                        dic_url[str_url] = True
                        obj_queue.put(str_url)
            time.sleep(1)
        list_ans = self._uniq(list_ans)
        self._output(list_ans)

list_entry = [
        'http://ip.jiangxianli.com/'
]
list_path_rules = [
        'http://ip.jiangxianli.com\?page\=[0-9]+'
]
list_data_rules = [
        'data-url=\"http[s]?://([0-9\.\:]+)'
]

spider = Spider(list_entry, list_path_rules, list_data_rules)
spider.run()
