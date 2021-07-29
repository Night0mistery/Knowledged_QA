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
        #����ʵ��������
        self.infos = ['name', 'desc', 'prevent', 'cause', 'easy_get', 'cure_department', 'cure_way', 'cure_lasttime', 'symptom',
             'cured_prob', 'get_prob']
        #������Ϣ�Ͷ�Ӧ��ʵ�����֮���ӳ��
        self.entities_infos_dict = {'common_drug': 'drug', 'recommand_drug': 'drug', 'not_eat': 'food', 'do_eat': 'food',
                           'recommand_eat': 'food', 'check': 'check', 'cure_department': 'department',
                           'name': 'name', 'symptom': 'symptom'}
        #��ϵ�������ʵ���������ӳ�䣺��ϵ��[������]
        self. relations_infos_dict = {'symptom': ['name', 'symptom'], 'acompany': ['name', 'name'],
                            'cure_department': ['name', 'department'], 'common_drug': ['name', 'drug'],
                            'recommand_drug': ['name', 'drug'], 'not_eat': ['name', 'food'],
                            'do_eat': ['name', 'food'], 'check': ['name', 'check'],
                            'recommand_eat': ['name', 'food']}
        #������������ؼ���
        self.qwds_dict = {'symptom':['֢״', '����', '����', '֢��', '����'],
                          'cause':['ԭ��', '����', 'Ϊʲô', '��ô��', '������', 'զ����', '������', '��λ�', 'Ϊɶ', 'Ϊ��', '��βŻ�', '��ô�Ż�', '�ᵼ��','�����'],
                          'acompany':['����֢', '����', 'һ����', 'һ������', 'һ�����', 'һ������', 'һͬ����', 'һͬ����', '���淢��', '����', '����'],
                          'food':['��ʳ', '����', '��', 'ʳ', '��ʳ', '��ʳ','��', '��', '�ɿ�', '��Ʒ', '����Ʒ', 'ʳ��', '����', 'ʳ��', 'ʳ��', '��Ʒ'],
                          'drug':['ҩ', 'ҩƷ', '��ҩ', '����', '�ڷ�Һ', '��Ƭ'],
                          'prevent':['Ԥ��', '����', '����', '����', '��ֹ', '���','�ӱ�', '�ܿ�', '���', '�ӿ�', '�ܿ�', '�ܵ�', '�㿪', '���', '�ƿ�', '�������ܲ�', '��ô���ܲ�', 'զ�����ܲ�', 'զ���ܲ�', '��β��ܲ�', '�����Ų�', '��ô�Ų�', 'զ���Ų�', 'զ�Ų�', '��βŲ�','�����ſ��Բ�', '��ô�ſ��Բ�', 'զ���ſ��Բ�', 'զ�ſ��Բ�', '��ο��Բ�', '�����ſɲ�', '��ô�ſɲ�', 'զ���ſɲ�', 'զ�ſɲ�', '��οɲ�'],
                          'last_time':['����', '���', '�೤ʱ��', '����ʱ��', '����','����', '������', '����Сʱ', '����Сʱ', '������'],
                          'cure_way':['��ô����', '���ҽ��', '��ôҽ��', '��ô��', '��ôҽ', '�����', 'ҽ�η�ʽ', '�Ʒ�', 'զ��', '��ô��', 'զ��', 'զ��'],
                          'cured_prob':['���������κ�', '��������κ�', '�κ�ϣ����ô', '����', '����', '����', '������', '����', '����', '������', '����ҽ'],
                          'easy_get':['�׸���Ⱥ', '���׸�Ⱦ', '�׷���Ⱥ', 'ʲô��', '��Щ��', '��Ⱦ','Ⱦ��', '����'],
                          'check':['���', '�����Ŀ', '���', '���', '���', '�Գ�'],
                          'belong':['����ʲô��', '����', 'ʲô��', '����'],
                          'cure':['����ʲô', '��ɶ', '����ɶ', 'ҽ��ɶ', '����ɶ', '����ɶ','����ʲô', '��ʲô��', '�к���', '�ô�', '��;', '��ʲô�ô�', '��ʲô�洦', '�к��洦', '����', '������ɶ', '��������', '��Ҫ', 'Ҫ']}
        #������������Ӧ�ؼ��ʡ�ʵ��֮���ӳ�䣺�������[[�ؼ����б�],[ʵ���б�]]
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
        #�������Ͷ�ӦҪ��ѯ�ĺ���ʵ������
        self.entity_parser_dict = {'disease_prevent': ['prevent'],
                              'disease_lasttime': ['last_time'],
                              'disease_cureway': ['cure_way'],
                              'disease_cureprob': ['cured_prob'],
                              'disease_easyget': ['easy_get'],
                              'disease_desc': ['desc'],
                              'disease_cause':['cause']}
        #�������Ͷ�ӦҪ��ѯ�Ĺ�ϵ
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
        #�ش�ģ��
        self.answer_dict = {'disease_symptom': '{m}��֢״������{n}',
                       'disease_acompany': '{m}�Ĳ���֢������{n}',
                       'disease_not_food': '{m}��ʳ��ʳ������У�{n}',
                       'disease_do_food': '{m}��ʳ��ʳ������У�{n}',
                       'food_do_disease': '����{m}���˽��������{n}',
                       'food_not_disease':'����{m}������ò�Ҫ��{n}',
                       'disease_drug': '{m}ͨ����ʹ�õ�ҩƷ������{n}',
                       'drug_disease': '{n}���εļ�����{m},��������',
                       'disease_check': '{m}ͨ������ͨ�����·�ʽ��������{n}',
                       'check_disease': 'ͨ������ͨ��{n}�������ļ�����{m}',
                       'symptom_disease': '֢״{n}����Ⱦ�ϵļ����У�{m}',
                       'disease_cause': '{m}���ܵĳ�����{n}',
                       'disease_prevent': '{m}��Ԥ����ʩ������{n}',
                       'disease_lasttime': '{m}�����ƿ��ܳ���������Ϊ��{n}',
                       'disease_cureway': '{m}���Գ����������ƣ�{n}',
                       'disease_cureprob': '{m}�����ĸ���Ϊ�������ο�����{n}',
                       'disease_easyget': '{m}���׸���Ⱥ������{n}',
                       'disease_desc': '{m}����Ϥһ�°���{n}'}
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
