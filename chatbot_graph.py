#!/usr/bin/env python3
# coding: utf-8

from question_classifier import QuestionClassifier
from question_parser import QuestionParser
from answer_search import AnswerSearcher

from src.redis_helper import RedisHelper
from backinfo import BackInfo


class ChatBotGraph:
    def __init__(self):
        self.backinfo = BackInfo()
        self.backinfo.load_info()
        self.backinfo.generate_yaml()
        self.backinfo.load_yaml()
        self.classifier = QuestionClassifier(self.backinfo.entities, self.backinfo.qwds_dict, self.backinfo.question_judge_dict)
        self.parser = QuestionParser(self.backinfo.entity_parser_dict,self.backinfo.relation_parser_dict,self.backinfo.relations_infos_dict,self.backinfo.question_judge_dict)
        self.searcher = AnswerSearcher(self.backinfo.entity_parser_dict,self.backinfo.relation_parser_dict,self.backinfo.answer_dict)

        self.redis = RedisHelper()
        self.redis.redis_restart()

        self.prefix = 'kg_'

    def chat_main(self, sent, user_id='000'):
        """
        问答系统主函数，包括背景知识录入，问题分类，问题查询，回答生成。
        """
        #加载回答模板
        answer = self.backinfo.templates['answer']
        fallback = self.backinfo.templates['fallback']
        restart = self.backinfo.templates['restart']
        ask_entity = self.backinfo.templates['ask_entity']
        ask_key_word = self.backinfo.templates['ask_key_word']
        # 重启问答系统
        args = {}
        if sent == 'restart':
            self.redis.redis_restart()
            return restart, args
        # 先到redis中拉取历史对话信息
        res_classify = self.classifier.classify(sent, user_id)
        print(res_classify)
        """
        sent:豆仁饭感冒可以吃吗
        res_classify: {'args': {'豆仁饭': ['food'], '感冒': ['disease']}, 
                        'question_types': ['disease_do_food', 'food_do_disease']}
        """
        if 'chitchat' in res_classify['question_types']:
            return fallback, args
        if  'no_entity' in res_classify['question_types']:
            return ask_entity, args
        if  'no_key_word' in res_classify['question_types']:
            temp = '、'.join(res_classify['args'].keys())
            ask_key_word = ask_key_word.format(temp)
            return ask_key_word, args

        args = res_classify['args']
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer, args
        else:
            return ('\n'.join(final_answers)), args


if __name__ == '__main__':
    bot = ChatBotGraph()
    while 1:
        question = input('用户:')
        if question == '退出':
            exit()
        answer, args = bot.chat_main(question, user_id='000')
        print('机器人:', answer)
