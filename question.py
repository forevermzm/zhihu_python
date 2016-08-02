# -*- coding: utf-8 -*-

'''Zhihu question object'''

import re
from soup_requester import SoupRequester


class Question:

    """Constructor"""
    def __init__(self, url):

        if not re.compile(r"(http|https)://www.zhihu.com/question/\d{8}").match(url):
            raise ValueError("\"" + url + "\"" + " : it isn't a question url.")

        self.url = url
        self.page_soup = SoupRequester.get_soup(self.url)

    def get_title(self):
        if self.page_soup.find("h2", class_="zm-item-title").string is not None:
            return self.page_soup.find("h2", class_="zm-item-title") \
                .string.encode("utf-8").replace("\n", "")
        else:
            return self.page_soup.find("span", class_="zm-editable-content") \
                .string.encode("utf-8").replace("\n", "")

    def get_detail(self):
        return self.page_soup.find("div", id="zh-question-detail").div.get_text().encode("utf-8")

    def get_answers_num(self):
        answers_num = 0
        if self.page_soup.find("h3", id="zh-question-answer-num") != None:
            answers_num = int(self.page_soup.find("h3", id="zh-question-answer-num")["data-num"])
        return answers_num

    def get_followers_num(self):
        return int(self.page_soup.find("div", class_="zg-gray-normal").a.strong.string)

    def get_topics(self):
        topic_list = self.page_soup.find_all("a", class_="zm-item-tag")
        topics = []
        for i in topic_list:
            topic = i.contents[0].string.encode("utf-8").replace("\n", "")
            topics.append(topic)
        return topics
