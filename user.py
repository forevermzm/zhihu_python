# -*- coding: utf-8 -*-

'''Zhihu User object'''

from soup_requester import SoupRequester
from question import Question

class User:
    latest_answer_base = "/answers?order_by=created&page="
    most_like_answer_base = "/answers?order_by=vote_num&page="

    def __init__(self, username):
        if username is None:
            raise ValueError(username + " cannot be empty.")
        self.username = username
        self.user_url = 'http://www.zhihu.com/people' + '/' + username
        self.page_soup = SoupRequester.get_soup(self.user_url)

    @classmethod
    # This is so ugly and change it later.
    def from_user_url(cls, user_url):
        base_url = 'www.zhihu.com/people/'
        if user_url.startswith(base_url, user_url.index('//') + 2) is False:
            raise ValueError("\"" + user_url + "\"" + " : it isn't a user url.")
        username = user_url[user_url.index(base_url) + len(base_url):]
        return cls(username)

    def refresh(self):
        self.page_soup = SoupRequester.get_soup(self.user_url)

    def get_followers_num(self):
        soup = self.page_soup
        followers_num = int(soup.find("div", class_="zm-profile-side-following zg-clear") \
                                                            .find_all("a")[1].strong.string)
        return followers_num

    def get_answers_num(self):
        soup = self.page_soup
        answers_num = int(soup.find_all("span", class_="num")[1].string)
        return answers_num

    def get_latest_20_answered_questions(self):
        return self.get_all_answered_questions(self.user_url + User.latest_answer_base, 3)

    def get_all_answered_questions(self, base_url, max_questions = None):
        answers_num = self.get_answers_num()
        if max_questions is not None:
            answers_num = min(answers_num, max_questions)
        # questions = []
        if answers_num != 0:
            for i in xrange((answers_num - 1) / 20 + 1):
                answer_url = base_url + str(i + 1)
                answer_soup = SoupRequester.get_soup(answer_url)
                for answer in answer_soup.find_all("a", class_="question_link"):
                    question_url = "http://www.zhihu.com" + answer["href"][0:18]
                    ques = Question(question_url)
                    yield ques
                    # questions.append(ques)
        # return questions


zhihu_user = User('giantchen')
print zhihu_user.get_followers_num()
print zhihu_user.get_answers_num()
for question in  zhihu_user.get_latest_20_answered_questions():
    print "Title: " + question.get_title()
    print "Description: " + question.get_detail()
    print "Topics: " + ' '.join(question.get_topics())
    print "========"
