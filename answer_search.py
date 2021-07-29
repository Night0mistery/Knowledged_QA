#!/usr/bin/env python3
# coding: utf-8

from py2neo import Graph


class AnswerSearcher:
    def __init__(self, entity_parser_dict, relation_parser_dict, answer_dict):
        # 设置密码，连接知识图谱
        self.g = Graph('http://localhost:7474/', auth=('neo4j', 'admin'))
        self.num_limit = 20
        self.entity_parser_dict = entity_parser_dict
        self.relation_parser_dict = relation_parser_dict
        self.answer_dict = answer_dict

    '''执行cypher查询，并返回相应结果'''

    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            for query in queries:
                answers = []
                ress = self.g.run(query).data()
                answers += ress
                #print(answers)
                final_answer = self.answer_prettify(question_type, answers)
                if final_answer:
                    final_answers.append(final_answer)
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''

    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        if question_type in self.entity_parser_dict.keys():
            desc = []
            for entity in self.entity_parser_dict[question_type]:
                for i in answers:
                    string = i['m.{0}'.format(entity)]
                    if string != None:
                        if isinstance(string,str):
                            desc.append(string)
                        elif isinstance(string,list):
                            desc.extend(string)
            subject = answers[0]['m.name']

        elif question_type in self.relation_parser_dict.keys():
            #relation = self.relation_parser_dict[question_type][1]
            if self.relation_parser_dict[question_type][0] =='m':
                desc = [i['n.name'] for i in answers]
                subject = answers[0]['m.name']
            elif self.relation_parser_dict[question_type][0] =='n':
                desc = [i['n.name'] for i in answers]
                subject = answers[0]['m.name']
        if desc == [None]:
            return ''
        final_answer = self.answer_dict[question_type].format(m=subject, n='；'.join(list(set(desc))[:self.num_limit]))

        """
        elif question_type == 'disease_symptom':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'symptom_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '症状{0}可能染上的疾病有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cause':
            desc = [i['m.cause'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}可能的成因有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_prevent':
            desc = [i['m.prevent'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的预防措施包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_lasttime':
            desc = [i['m.lasttime'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}治疗可能持续的周期为：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cureway':
            desc = [';'.join(i['m.cure_way']) for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}可以尝试如下治疗：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cureprob':
            desc = [i['m.cured_prob'] for i in answers]
            print('desc',desc)
            subject = answers[0]['m.name']
            final_answer = '{0}治愈的概率为（仅供参考）：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_easyget':
            desc = [i['m.easy_get'] for i in answers]
            subject = answers[0]['m.name']

            final_answer = '{0}的易感人群包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_desc':
            desc = [i['m.desc'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0},熟悉一下：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_acompany':
            desc1 = [i['n.name'] for i in answers]
            desc2 = [i['m.name'] for i in answers]
            subject = answers[0]['m.name']
            desc = [i for i in desc1 + desc2 if i != subject]
            final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_not_food':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}忌食的食物包括有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_do_food':
            do_desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}宜食的食物包括有：{1}'.format(subject, ';'.join(list(set(do_desc))[:self.num_limit]))

        elif question_type == 'food_not_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '患有{0}的人最好不要吃{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)

        elif question_type == 'food_do_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '患有{0}的人建议多试试{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)

        elif question_type == 'disease_drug':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}通常的使用的药品包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'drug_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '{0}主治的疾病有{1},可以试试'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_check':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}通常可以通过以下方式检查出来：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'check_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '通常可以通过{0}检查出来的疾病有{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        """
        return final_answer


if __name__ == '__main__':
    from backinfo import BackInfo

    backinfo = BackInfo()
    searcher = AnswerSearcher(backinfo.entity_parser_dict,backinfo.relation_parser_dict,backinfo.answer_dict)
    ans = searcher.search_main([{'question_type': 'disease_symptom',
      'sql': ["MATCH (m:name)-[r:symptom]->(n:symptom) where m.name = '非典' return "
              'm.name, r.name, n.name',
              "MATCH (m:name)-[r:symptom]->(n:symptom) where m.name = '感冒' return "
              'm.name, r.name, n.name']},
     {'question_type': 'symptom_disease',
      'sql': ["MATCH (m:name)-[r:symptom]->(n:symptom) where n.name = '流鼻涕' return "
              'm.name, r.name, n.name']}])

    print(ans)
