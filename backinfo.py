# coding=gbk
from exc_json import achieve_data
from ruamel import yaml
from pprint import pprint

# back infos for the dialog
class BackInfo:
    def __init__(self):
        # config info path
        self.excel_path = './backinfo/backinfo.xlsx'
        self.yaml_path = './backinfo/backinfo.yaml'
        #self.load_info()
        """
        self.entities = ['drug', 'food', 'check', 'department', 'name', 'symptom']
        #核心实体属性名
        self.infos = ['name', 'desc', 'prevent', 'cause', 'easy_get', 'cure_department', 'cure_way', 'cure_lasttime', 'symptom',
             'cured_prob', 'get_prob']
        #数据信息和对应的实体类别之间的映射
        self.entities_infos_dict = {'common_drug': 'drug', 'recommand_drug': 'drug', 'not_eat': 'food', 'do_eat': 'food',
                           'recommand_eat': 'food', 'check': 'check', 'cure_department': 'department',
                           'name': 'name', 'symptom': 'symptom'}
        #关系类别名和实体类别名的映射：关系：[主，客]
        self. relations_infos_dict = {'symptom': ['name', 'symptom'], 'acompany': ['name', 'name'],
                            'cure_department': ['name', 'department'], 'common_drug': ['name', 'drug'],
                            'recommand_drug': ['name', 'drug'], 'not_eat': ['name', 'food'],
                            'do_eat': ['name', 'food'], 'check': ['name', 'check'],
                            'recommand_eat': ['name', 'food']}
        #各个类别的问题关键词
        self.qwds_dict = {'symptom':['症状', '表征', '现象', '症候', '表现'],
                          'cause':['原因', '成因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会', '为啥', '为何', '如何才会', '怎么才会', '会导致','会造成'],
                          'acompany':['并发症', '并发', '一起发生', '一并发生', '一起出现', '一并出现', '一同发生', '一同出现', '伴随发生', '伴随', '共现'],
                          'food':['饮食', '饮用', '吃', '食', '伙食', '膳食','喝', '菜', '忌口', '补品', '保健品', '食谱', '菜谱', '食用', '食物', '补品'],
                          'drug':['药', '药品', '用药', '胶囊', '口服液', '炎片'],
                          'prevent':['预防', '防范', '抵制', '抵御', '防止', '躲避','逃避', '避开', '免得', '逃开', '避开', '避掉', '躲开', '躲掉', '绕开', '怎样才能不', '怎么才能不', '咋样才能不', '咋才能不', '如何才能不', '怎样才不', '怎么才不', '咋样才不', '咋才不', '如何才不','怎样才可以不', '怎么才可以不', '咋样才可以不', '咋才可以不', '如何可以不', '怎样才可不', '怎么才可不', '咋样才可不', '咋才可不', '如何可不'],
                          'last_time':['周期', '多久', '多长时间', '多少时间', '几天','几年', '多少天', '多少小时', '几个小时', '多少年'],
                          'cure_way':['怎么治疗', '如何医治', '怎么医治', '怎么治', '怎么医', '如何治', '医治方式', '疗法', '咋治', '怎么办', '咋办', '咋治'],
                          'cured_prob':['多大概率能治好', '多大几率能治好', '治好希望大么', '几率', '几成', '比例', '可能性', '能治', '可治', '可以治', '可以医'],
                          'easy_get':['易感人群', '容易感染', '易发人群', '什么人', '哪些人', '感染','染上', '得上'],
                          'check':['检查', '检查项目', '查出', '检查', '测出', '试出'],
                          'belong':['属于什么科', '属于', '什么科', '科室'],
                          'cure':['治疗什么', '治啥', '治疗啥', '医治啥', '治愈啥', '主治啥','主治什么', '有什么用', '有何用', '用处', '用途', '有什么好处', '有什么益处', '有何益处', '用来', '用来做啥', '用来作甚', '需要', '要']}
        #问题类别名与对应关键词、实体之间的映射：问题类别[[关键词列表],[实体列表]]
        self.question_judge_dict = {'disease_symptom': [['symptom'], ['name']],
                               'symptom_disease': [[], ['symptom']],
                               'disease_cause': [['cause'], ['name']],
                               'disease_acompany': [['acompany'], ['name']],
                               'disease_not_food': [['food', 'deny'], ['name']],
                               'disease_do_food': [['food'], ['name']],
                               'food_not_disease': [['food', 'deny'], ['food']],
                               'food_do_disease': [['food'], ['food']],
                               'disease_drug': [['drug'], ['name']],
                               'drug_disease': [['cure'], ['drug']],
                               'disease_check': [['check'], ['name']],
                               'check_disease': [['check'], ['check']],
                               'disease_prevent': [['prevent'], ['name']],
                               'disease_lasttime': [['last_time'], ['name']],
                               'disease_cureway': [['cure_way'], ['name']],
                               'disease_cureprob': [['cured_prob'], ['name']],
                               'disease_easyget': [['easy_get'], ['name']],
                               'disease_desc': [[], ['name']]}
        #问题类别和对应要查询的核心实体属性
        self.entity_parser_dict = {'disease_prevent': ['prevent'],
                              'disease_lasttime': ['last_time'],
                              'disease_cureway': ['cure_way'],
                              'disease_cureprob': ['cured_prob'],
                              'disease_easyget': ['easy_get'],
                              'disease_desc': ['desc'],
                              'disease_cause':['cause']}
        #问题类别和对应要查询的关系
        self.relation_parser_dict = {'disease_symptom': ['m', 'symptom'],
                                'symptom_disease': ['n', 'symptom'],
                                'disease_acompany': ['m', 'acompany'],
                                'disease_not_food': ['m', 'not_eat'],
                                'disease_do_food': ['m', 'do_eat'],
                                'food_not_disease': ['n', 'not_eat'],
                                'food_do_disease': ['n', 'do_eat'],
                                'disease_drug': ['m', 'common_drug'],
                                'drug_disease': ['n', 'common_drug'],
                                'disease_check': ['m', 'check'],
                                'check_disease': ['n', 'check']}
        #回答模板
        self.answer_dict = {'disease_symptom': '{m}的症状包括：{n}',
                       'disease_acompany': '{m}的并发症包括：{n}',
                       'disease_not_food': '{m}忌食的食物包括有：{n}',
                       'disease_do_food': '{m}宜食的食物包括有：{n}',
                       'food_do_disease': '患有{m}的人建议多试试{n}',
                       'food_not_disease':'患有{m}的人最好不要吃{n}',
                       'disease_drug': '{m}通常的使用的药品包括：{n}',
                       'drug_disease': '{n}主治的疾病有{m},可以试试',
                       'disease_check': '{m}通常可以通过以下方式检查出来：{n}',
                       'check_disease': '通常可以通过{n}检查出来的疾病有{m}',
                       'symptom_disease': '症状{n}可能染上的疾病有：{m}',
                       'disease_cause': '{m}可能的成因有{n}',
                       'disease_prevent': '{m}的预防措施包括：{n}',
                       'disease_lasttime': '{m}的治疗可能持续的周期为：{n}',
                       'disease_cureway': '{m}可以尝试如下治疗：{n}',
                       'disease_cureprob': '{m}治愈的概率为（仅供参考）：{n}',
                       'disease_easyget': '{m}的易感人群包括：{n}',
                       'disease_desc': '{m}，熟悉一下啊：{n}'}
        """

    def load_info(self):
        print('Loading backinfo...')
        info = achieve_data(self.excel_path)
        if info is not None:
            worksheets = info.sheet_names()
            print('sheets index and name:')
            for index, sheet in enumerate(worksheets):
                print(index, sheet)
            self.entities, self.infos, self.entities_infos_dict = self.load_entities(info)
            self.relations_infos_dict = self.load_relations(info)
            self.qwds_dict = self.load_key_words(info)
            self.question_judge_dict, self.entity_parser_dict, self.relation_parser_dict, self.answer_dict = self.load_questions(info)
            self.templates = self.load_templates(info)
            print('Load all infos successfully!')

    def generate_yaml(self):
        with open(self.yaml_path, "w", encoding="utf-8") as file:
            yaml.dump({'entities': self.entities}, file, Dumper=yaml.RoundTripDumper, default_flow_style=False, allow_unicode=True, indent=4)
            yaml.dump({'infos': self.infos}, file, Dumper=yaml.RoundTripDumper, default_flow_style=False, allow_unicode=True, indent=4)
            yaml.dump({'relations_infos_dict': self.relations_infos_dict}, file, Dumper=yaml.RoundTripDumper, default_flow_style=False, allow_unicode=True, indent=4)
            yaml.dump({'qwds_dict': self.qwds_dict}, file, Dumper=yaml.RoundTripDumper, default_flow_style=False, allow_unicode=True, indent=4)
            yaml.dump({'question_judge_dict': self.question_judge_dict}, file, Dumper=yaml.RoundTripDumper, default_flow_style=False, allow_unicode=True, indent=4)
            yaml.dump({'entity_parser_dict': self.entity_parser_dict}, file, Dumper=yaml.RoundTripDumper, default_flow_style=False, allow_unicode=True, indent=4)
            yaml.dump({'relation_parser_dict': self.relation_parser_dict}, file, Dumper=yaml.RoundTripDumper, default_flow_style=False, allow_unicode=True, indent=4)
            yaml.dump({'answer_dict': self.answer_dict}, file, Dumper=yaml.RoundTripDumper, default_flow_style=False, allow_unicode=True, indent=4)
            yaml.dump({'templates': self.templates}, file, Dumper=yaml.RoundTripDumper, default_flow_style=False, allow_unicode=True, indent=4)
            print('Generate yaml successfully!')

    def load_yaml(self):
        with open(self.yaml_path, "r", encoding="utf-8") as file:
            b_info = yaml.load(file)
            self.entities = b_info['entities']
            self.infos = b_info['infos']
            self.relations_infos_dict = b_info['relations_infos_dict']
            self.qwds_dict = b_info['qwds_dict']
            self.question_judge_dict = b_info['question_judge_dict']
            self.entity_parser_dict = b_info['entity_parser_dict']
            self.relation_parser_dict = b_info['relation_parser_dict']
            self.answer_dict = b_info['answer_dict']
            self.templates = b_info['templates']
            print('Load yaml successfully!')
            #pprint(b_info)

    def load_entities(self, info, sheet_index=0):
        sheet = info.sheet_by_index(sheet_index)
        entities = sheet.row_values(0)
        infos = []
        entities_infos_dict = {}
        for i in range(1, sheet.nrows):
            row = sheet.row_values(i)
            for index, entity in enumerate(entities):
                if row[index] != '':
                    if entity == 'name':
                        infos.append(row[index])
                    else:
                        entities_infos_dict[row[index]] = entity
        print('Load entities successfully!')
        return entities, infos, entities_infos_dict

    def load_relations(self, info, sheet_index=1):
        sheet = info.sheet_by_index(sheet_index)
        relations_infos_dict = {}
        for i in range(sheet.nrows):
            row = sheet.row_values(i)
            relations_infos_dict[row[0]] = [row[1],row[2]]
        print('Load relations successfully!')
        return relations_infos_dict

    def load_key_words(self, info, sheet_index=2):
        sheet = info.sheet_by_index(sheet_index)
        qwds_dict = {}
        for i in range(sheet.nrows):
            row = sheet.row_values(i)
            qwds_dict[row[0]] = [row[j] for j in range(1, len(row)) if row[j] != '']
        print('Load key words successfully!')
        return qwds_dict

    def load_questions(self, info, sheet_index=3):
        sheet = info.sheet_by_index(sheet_index)
        titles = sheet.row_values(0)
        question_judge_dict, entity_parser_dict, relation_parser_dict, answer_dict = {}, {}, {}, {}
        for i in range(1, sheet.nrows):
            row = sheet.row_values(i)
            key = row[0]
            if '|' in row[1]:
                row[1] = row[1].split('|')
            elif row[1] == '':
                row[1] = []
            else:
                row[1] = [row[1]]
            if '|' in row[2]:
                row[2] = row[2].split('|')
            elif row[2] == '':
                row[2] = []
            else:
                row[2] = [row[2]]
            question_judge_dict[key] = [row[1], row[2]]
            if row[3] != '':
                entity_parser_dict[key] = row[3]
            else:
                relation_parser_dict[key] = [row[4], row[5]]
            answer_dict[key] = row[6]
        print('Load questions successfully!')
        return question_judge_dict, entity_parser_dict, relation_parser_dict, answer_dict

    def load_templates(self, info, sheet_index=4):
        sheet = info.sheet_by_index(sheet_index)
        templates_dict = {}
        for i in range(0, sheet.nrows):
            row = sheet.row_values(i)
            templates_dict[row[1]] = row[2]
        print('Load templates successfully!')
        return templates_dict

if __name__ == '__main__':
    #test load data
    backinfo = BackInfo()
    backinfo.load_info()
    backinfo.generate_yaml()
    backinfo.load_yaml()
    """
    backinfo.load_info()
    from pprint import pprint
    print('entities = ')
    pprint(backinfo.entities)
    print('infos = ')
    pprint(backinfo.infos)
    print('entities_infos_dict = ')
    pprint(backinfo.entities_infos_dict)
    print('relations_infos_dict = ')
    pprint(backinfo.relations_infos_dict)
    print('qwds_dict = ')
    pprint( backinfo.qwds_dict)
    print('question_judge_dict = ')
    pprint(backinfo.question_judge_dict)
    print('entity_parser_dict = ')
    pprint(backinfo.entity_parser_dict)
    print('relation_parser_dict = ')
    pprint(backinfo.relation_parser_dict)
    print('answer_dict = ')
    pprint(backinfo.answer_dict)
    print('templates = ')
    pprint(backinfo.templates)
    """
