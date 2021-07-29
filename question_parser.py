#!/usr/bin/env python3
# coding: utf-8

class QuestionParser:
    def __init__(self,entity_parser_dict,relation_parser_dict,relations_infos_dict,question_judge_dict):
        self.entity_parser_dict = entity_parser_dict
        self.relation_parser_dict = relation_parser_dict
        self.relations_infos_dict = relations_infos_dict
        self.question_judge_dict = question_judge_dict

    def build_entitydict(self, args):
        """构建实体节点"""
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    def parser_main(self, res_classify):
        """解析主函数"""
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        #print(entity_dict, question_types)
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = self.sql_transfer(question_type, entity_dict.get(self.question_judge_dict[question_type][1][0]))
            """
            if question_type == 'disease_symptom':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'symptom_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('symptom'))

            elif question_type == 'disease_cause':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_acompany':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_not_food':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_do_food':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'food_not_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('food'))

            elif question_type == 'food_do_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('food'))

            elif question_type == 'disease_drug':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'drug_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))

            elif question_type == 'disease_check':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'check_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('check'))

            elif question_type == 'disease_prevent':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_lasttime':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_cureway':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_cureprob':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_easyget':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))
            """
            #pprint(sql)
            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)
        #print("sqls:",sqls)
        return sqls

    def sql_transfer(self, question_type, entities):
        """
        针对不同的问题，分开进行处理，主要分为查找某实体的属性，或查找与实体有某关系的实体
        1、查找实体的属性  MATCH (m:Disease) where m.name = '疾病名' return m.name, m.cause
        2、查找与实体有某关系的实体
        MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where m.name = '{0}' return m.name, r.name, n.name
        """
        if not entities:
            return []
        sql = []
        # 查询疾病的原因

        #ask for entity
        if question_type in self.entity_parser_dict.keys():
            infos = self.entity_parser_dict[question_type]
            sql = ["m.{0}".format(i) for i in infos]
            sql = ["MATCH (m:name) where m.name = '{0}' return m.name, {1}".format(i, ', '.join(sql)) for i in entities]
        #ask for relation
        elif question_type in self.relation_parser_dict.keys():
            obj = self.relation_parser_dict[question_type][0]
            relation = self.relation_parser_dict[question_type][1]
            sql = ["MATCH (m:{0})-[r:{1}]->(n:{2}) where {3}.name = '{4}' return m.name, r.name, n.name".format(self.relations_infos_dict[relation][0],relation,self.relations_infos_dict[relation][1],obj,i) for i in entities]
        """
        if question_type == 'disease_cause':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cause".format(i) for i in entities]

        # 查询疾病的防御措施
        elif question_type == 'disease_prevent':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.prevent".format(i) for i in entities]

        # 查询疾病的持续时间
        elif question_type == 'disease_lasttime':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cure_lasttime".format(i) for i in entities]

        # 查询疾病的治愈概率
        elif question_type == 'disease_cureprob':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cured_prob".format(i) for i in entities]

        # 查询疾病的治疗方式
        elif question_type == 'disease_cureway':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cure_way".format(i) for i in entities]

        # 查询疾病的易发人群
        elif question_type == 'disease_easyget':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.easy_get".format(i) for i in entities]

        # 查询疾病的相关介绍
        elif question_type == 'disease_desc':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.desc".format(i) for i in entities]

        # 查询疾病有哪些症状
        elif question_type == 'disease_symptom':
            sql = [
                "MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where m.name = '{0}' return m.name, r.name, n.name".format(
                    i) for i in entities]

        # 查询症状会导致哪些疾病
        elif question_type == 'symptom_disease':
            sql = [
                "MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '{0}' return m.name, r.name, n.name".format(
                    i) for i in entities]

        # 查询疾病的并发症
        elif question_type == 'disease_acompany':
            sql1 = [
                "MATCH (m:Disease)-[r:acompany_with]->(n:Disease) where m.name = '{0}' return m.name, r.name, n.name".format(
                    i) for i in entities]
            sql2 = [
                "MATCH (m:Disease)-[r:acompany_with]->(n:Disease) where n.name = '{0}' return m.name, r.name, n.name".format(
                    i) for i in entities]
            sql = sql1 + sql2
        # 查询疾病的忌口
        elif question_type == 'disease_not_food':
            sql = ["MATCH (m:Disease)-[r:no_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i)
                   for i in entities]

        # 查询疾病建议吃的东西
        elif question_type == 'disease_do_food':
            sql1 = [
                "MATCH (m:Disease)-[r:do_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i)
                for i in entities]
            sql2 = [
                "MATCH (m:Disease)-[r:recommand_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(
                    i) for i in entities]
            sql = sql1 + sql2

        # 已知忌口查疾病
        elif question_type == 'food_not_disease':
            sql = ["MATCH (m:Disease)-[r:no_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i)
                   for i in entities]

        # 已知推荐查疾病
        elif question_type == 'food_do_disease':
            sql1 = [
                "MATCH (m:Disease)-[r:do_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i)
                for i in entities]
            sql2 = [
                "MATCH (m:Disease)-[r:recommand_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(
                    i) for i in entities]
            sql = sql1 + sql2

        # 查询疾病常用药品－药品别名记得扩充
        elif question_type == 'disease_drug':
            sql1 = [
                "MATCH (m:Disease)-[r:common_drug]->(n:Drug) where m.name = '{0}' return m.name, r.name, n.name".format(
                    i) for i in entities]
            sql2 = [
                "MATCH (m:Disease)-[r:recommand_drug]->(n:Drug) where m.name = '{0}' return m.name, r.name, n.name".format(
                    i) for i in entities]
            sql = sql1 + sql2

        # 已知药品查询能够治疗的疾病
        elif question_type == 'drug_disease':
            sql1 = [
                "MATCH (m:Disease)-[r:common_drug]->(n:Drug) where n.name = '{0}' return m.name, r.name, n.name".format(
                    i) for i in entities]
            sql2 = [
                "MATCH (m:Disease)-[r:recommand_drug]->(n:Drug) where n.name = '{0}' return m.name, r.name, n.name".format(
                    i) for i in entities]
            sql = sql1 + sql2
        # 查询疾病应该进行的检查
        elif question_type == 'disease_check':
            sql = [
                "MATCH (m:Disease)-[r:need_check]->(n:Check) where m.name = '{0}' return m.name, r.name, n.name".format(
                    i) for i in entities]

        # 已知检查查询疾病
        elif question_type == 'check_disease':
            sql = [
                "MATCH (m:Disease)-[r:need_check]->(n:Check) where n.name = '{0}' return m.name, r.name, n.name".format(
                    i) for i in entities]
        """
        return sql


if __name__ == '__main__':
    from pprint import pprint
    from backinfo import BackInfo

    backinfo = BackInfo()
    handler = QuestionParser(backinfo.entity_parser_dict,backinfo.relation_parser_dict,backinfo.relations_infos_dict,backinfo.question_judge_dict)
    # sql = handler.parser_main({'args': {'豆仁饭': ['food'], '感冒': ['disease']},
    #                            'question_types': ['disease_do_food', 'food_do_disease']})
    sqls = handler.parser_main({'args': {'非典': ['name'], '感冒': ['name'],'流鼻涕':['symptom']},
                               'question_types': ['disease_symptom','symptom_disease']})
    #sqls =handler.parser_main({'args': {'流鼻涕': ['symptom']}, 'question_types': ['symptom_disease']})
    pprint(sqls)
