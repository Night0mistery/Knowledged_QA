#!/usr/bin/env python3
# coding: utf-8

import os
import ahocorasick

from src.redis_helper import RedisHelper
from src.tireTree import Trie
from src.KeywordProcessor import KeywordProcessor
import copy
from backinfo import BackInfo


class QuestionClassifier:
    def __init__(self, entities, qwds_dict, question_judge_dict):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        # redis
        self.prefix = 'kg_'
        self.redis = RedisHelper()
        # 　特征词路径
        self.entities = entities
        self.path_dict = dict()
        for entity in entities:
            self.path_dict[entity] = os.path.join(cur_dir, 'dict/%s.txt' % entity)
        self.path_dict['deny'] = os.path.join(cur_dir, 'dict/deny.txt')
        # 加载特征词，根据特征词确定实体
        # 目前有疾病、科室、药品、实物、并发症、诊断检查项目、在售药品
        self.region_words = []
        self.deny_words = [i.strip() for i in open(self.path_dict['deny'], encoding='UTF-8') if i.strip()]
        self.wds_dict = dict()
        for entity in self.entities:
            self.wds_dict[entity] = [i.strip() for i in open(self.path_dict[entity], encoding='UTF-8') if i.strip()]
        for words in self.wds_dict.values():
            self.region_words = self.region_words + words
        self.region_words = set(self.region_words)
        # 构建字典树
        self.region_tree = Trie()
        for word in list(self.region_words):
            self.region_tree.add(word)
        # self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典  词：类型
        self.wdtype_dict = self.build_wdtype_dict()
        # 问句疑问词
        qwds_dict['deny'] = self.deny_words
        self.qwds_dict = qwds_dict
        # self.qwds_type = list(qwds_dict.keys())
        self.question_judge_dict = question_judge_dict
        # 构建关键词
        self.kp = KeywordProcessor()
        print('model init successfully！')

        return

    def judge_qes(self, entity_types, key_word_types, ls_state):
        # TODO 问答类型这一部分可以用flashtext加快查找速度
        question_types = []
        # question_type = 'others'
        # 无实体有问题类型，向用户查询问题类型
        if entity_types and not key_word_types:
            question_types = ['no_key_word']
        # 有实体无问题类型，向用户查询问题类型
        elif key_word_types and not entity_types:
            question_types = ['no_entity']
        else:
            for q_type, v in self.question_judge_dict.items():
                key_word_list = v[0]
                entity_type_list = v[1]
                if key_word_list and entity_type_list:
                    flag = 1
                    for word in key_word_list:
                        if word not in key_word_types:
                            flag = 0
                    for e_type in entity_type_list:
                        if e_type not in entity_types:
                            flag = 0
                        # print('check entity:',q_type, flag)
                    if flag:
                        question_types.append(q_type)

        """
        if question_types == []:
            for q_type, v in self.question_judge_dict.items():
                key_word_list = v[0]
                entity_type_list = v[1]
                if key_word_list == [] and entity_type_list:
                    flag = 1
                    for e_type in entity_type_list:
                        if e_type not in types:
                            flag = 0
                    if flag:
                        question_types.append(q_type)
        """
        """
        # 症状
        if self.check_words(self.symptom_qwds, question) and ('disease' in types):
            question_type = 'disease_symptom'
            question_types.append(question_type)

        # 症状可能的疾病
        if self.check_words(self.symptom_qwds, question) and ('symptom' in types):
            question_type = 'symptom_disease'
            question_types.append(question_type)
        # 原因
        if self.check_words(self.cause_qwds, question) and ('disease' in types):
            question_type = 'disease_cause'
            question_types.append(question_type)
        # 并发症
        if self.check_words(self.acompany_qwds, question) and ('disease' in types):
            question_type = 'disease_acompany'
            question_types.append(question_type)
        # 推荐食品（某种疾病可以吃，不能吃）
        if self.check_words(self.food_qwds, question) and 'disease' in types:
            deny_status = self.check_words(self.deny_words, question)
            if deny_status:
                question_type = 'disease_not_food'
            else:
                question_type = 'disease_do_food'
            question_types.append(question_type)
        # 已知食物找疾病（哪些人最好（不）吃某种food）
        if self.check_words(self.food_qwds + self.cure_qwds, question) and 'food' in types:
            deny_status = self.check_words(self.deny_words, question)
            if deny_status:
                question_type = 'food_not_disease'
            else:
                question_type = 'food_do_disease'
            question_types.append(question_type)
        # 推荐药品（啥病要吃啥药）
        if self.check_words(self.drug_qwds, question) and 'disease' in types:
            question_type = 'disease_drug'
            question_types.append(question_type)
        # 药品治啥病（啥药可以治啥病）
        if self.check_words(self.cure_qwds, question) and 'drug' in types:
            question_type = 'drug_disease'
            question_types.append(question_type)
        # 疾病接受检查项目
        if self.check_words(self.check_qwds, question) and 'disease' in types:
            question_type = 'disease_check'
            question_types.append(question_type)
        # 已知检查项目查相应疾病
        if self.check_words(self.check_qwds + self.cure_qwds, question) and 'check' in types:
            question_type = 'check_disease'
            question_types.append(question_type)
        # 　症状防御
        if self.check_words(self.prevent_qwds, question) and 'disease' in types:
            question_type = 'disease_prevent'
            question_types.append(question_type)
        # 疾病医疗周期
        if self.check_words(self.lasttime_qwds, question) and 'disease' in types:
            question_type = 'disease_lasttime'
            question_types.append(question_type)
        # 疾病治疗方式
        if self.check_words(self.cureway_qwds, question) and 'disease' in types:
            question_type = 'disease_cureway'
            question_types.append(question_type)
        # 疾病治愈可能性
        if self.check_words(self.cureprob_qwds, question) and 'disease' in types:
            question_type = 'disease_cureprob'
            question_types.append(question_type)
        # 疾病易感染人群
        if self.check_words(self.easyget_qwds, question) and 'disease' in types:
            question_type = 'disease_easyget'
            question_types.append(question_type)
        """
        # 没有查询到问句信息，从上一轮中拉取
        if not question_types:
            question_types = ls_state['question_types']
        """
        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if question_types == [] and 'disease' in types:
            question_types = ['disease_desc']
        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if question_types == [] and 'symptom' in types:
            question_types = ['symptom_disease']
        """

        return question_types

    def check_key_words(self, question):
        keys = list()
        for key, values in self.qwds_dict.items():
            for value in values:
                if value in question:
                    keys.append(key)
        return keys

    def classify(self, question, user_id):
        """
        问题分类主函数
        传入用户问题、redis类、用户id
        """
        ls_state = self.redis.key_get(self.prefix + user_id)
        cur_state = copy.deepcopy(ls_state)

        # 提取问题中的实体
        question_entity_dict = self.check_entity(question)
        # 提取问题中的关键词类型
        question_key_word_types = self.check_key_words(question)

        # 若当前句子无实体也无问题类型，判断为chitchat，不更新状态
        if not question_entity_dict and not question_key_word_types:
            return {'args': {}, 'key_word_types': [], 'question_types': ['chitchat']}

        # 若当前句子无关键词有实体
        elif not question_key_word_types:
            # 拉取上轮关键词类型
            if ls_state['key_word_types']:
                question_key_word_types = ls_state['key_word_types']
            # 关键词缺失
            else:
                cur_state['key_word_types'] = []
            cur_state['args'] = question_entity_dict

        # 若当前句子无实体有关键词
        elif not question_entity_dict:
            # 拉取上轮实体
            if ls_state['args']:
                question_entity_dict = ls_state['args']
            # 实体缺失
            else:
                cur_state['args'] = {}
            cur_state['key_word_types'] = question_key_word_types
        else:
            cur_state['args'] = question_entity_dict
            cur_state['key_word_types'] = question_key_word_types

        # 收集问句当中所涉及到的实体类型
        types = []
        for type_ in question_entity_dict.values():
            types.extend(list(type_))
        types = list(set(types))

        # 更新当前问题类型
        cur_state['question_types'] = self.judge_qes(types, question_key_word_types, ls_state)

        # 更新状态
        self.redis.key_insert(self.prefix + user_id, cur_state)

        # TODO 如果ls_state == cur_state默认为用户当前句并没有提及到任何有用的信息
        # if ls_state == cur_state:
        #     return {}
        #print(cur_state)
        return cur_state

    def build_wdtype_dict(self):
        """构造词对应的类型"""

        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            """
            if wd in self.name_wds:
                wd_dict[wd].append('disease')
            if wd in self.department_wds:
                wd_dict[wd].append('department')
            if wd in self.check_wds:
                wd_dict[wd].append('check')
            if wd in self.drug_wds:
                wd_dict[wd].append('drug')
            if wd in self.food_wds:
                wd_dict[wd].append('food')
            if wd in self.symptom_wds:
                wd_dict[wd].append('symptom')
            if wd in self.producer_wds:
                wd_dict[wd].append('producer')
            """
            for entity in self.entities:
                if wd in self.wds_dict[entity]:
                    wd_dict[wd].append(entity)

        return wd_dict

    def build_actree(self, wordlist):
        """构造actree，加速过滤"""
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    def check_medical(self, question):
        """问句过滤"""
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i: self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

    def check_entity(self, question):
        entity = self.region_tree.find_entity(str(question), longest=True, drop_duplicates=True)
        final_dict = {item: self.wdtype_dict.get(item) for item in entity.values()}
        return final_dict


if __name__ == '__main__':
    """
        sent:豆仁饭感冒可以吃吗
        res_classify: {'args': {'豆仁饭': ['food'], '感冒': ['disease']}, 
                        'question_types': ['disease_do_food', 'food_do_disease']}
    """
    backinfo = BackInfo()
    handler = QuestionClassifier(backinfo.entities, backinfo.qwds_dict, backinfo.question_judge_dict)
    while 1:
        question = input('input an question:')
        data = handler.classify(question, user_id='0000')
        print(data)
