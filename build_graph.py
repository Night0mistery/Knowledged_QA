#!/usr/bin/env python3
# coding: utf-8
# File: AnyGraph.py
# Date: 21-7-6

import os
import json
from py2neo import Graph, Node
from backinfo import BackInfo
from tqdm import tqdm

class AnyGraph:
    def __init__(self,entities,infos,entities_infos_dict,relations_infos_dict):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, 'data/test_large.json')
        self.g = Graph('http://localhost:7474/',auth=('neo4j','admin'))
        # neo4j 搭载服务器的ip地址，ifconfig可获取到 neo4j，服务器监听的端口号数据库user name，如果没有更改过，应该是neo4j

        sql = "MATCH (n)-[r]->() RETURN COUNT(n), COUNT(r)"
        print(self.g.run(sql).data())

        # 删除
        self.g.run("MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r")
        print(self.g.run(sql).data())
        self.g.delete_all()

        # 实体类型，info类型，关系类型，实体标签对应关系，关系标签对应关系
        relations = []
        for key in relations_infos_dict.keys():
            relations.append(key)
        self.entities = entities
        self.infos = infos
        self.relations = relations
        self.entities_infos_dict = entities_infos_dict
        self.relations_infos_dict = relations_infos_dict

        #读取数据
        self.entities_dict, self.entity_infos, self.relations_dict = self.read_nodes_test()
        # exit()

    '''读取文件'''
    def empty_dict(self, key_list):
        result_dict = {}
        for key in key_list:
            result_dict[key] = []
        return result_dict

    def read_nodes_test(self):

        entities_dict = self.empty_dict(self.entities)
        relations_dict = self.empty_dict(self.relations)
        #properties_dict = self.empty_dict(self.properties)
        entity_infos = []

        # Data must have name!
        count = 0
        with open(self.data_path, encoding='UTF-8') as f:
            data = json.load(f)
        for data_json in data:
            infos_dict = self.empty_dict(self.infos)
            #Use count if the data size is too large
            count += 1
            if count == 1000:
                break
            if 'name' in data_json.keys() == 0:
                # print(data_json.keys())
                # print(data_json['name'])
                print('Error!')
            name = data_json['name']
            print('loading entity:', data_json['name'])

            for key in data_json:
                if key in infos_dict.keys():
                    infos_dict[key] = data_json[key]
                entities_dict['name'].append(data_json['name'])
                if key in self.entities_infos_dict.keys():
                    value = self.entities_infos_dict[key]
                    if isinstance(data_json[key], str):
                        entities_dict[value].append(data_json[key])
                    elif isinstance(data_json[key], list):
                        entities_dict[value] += data_json[key]
                    else:
                        # to be add
                        pass
                if key in relations_dict.keys():
                    for value in data_json[key]:
                        relations_dict[key].append([name, value])
            entity_infos.append(infos_dict)
        return entities_dict, entity_infos, relations_dict

    '''建立节点'''
    def create_node(self, label, nodes):
        count = 0
        with tqdm(total=len(nodes)) as pbar:
            pbar.set_description("Processing %s node"%label)
            for node_name in nodes:
                node = Node(label, name=node_name)
                self.g.create(node)
                count += 1
                pbar.update(1)
                #print('node count:', node_name, count, len(nodes))
        return

    '''创建知识图谱中心疾病的节点'''
    def create_central_nodes(self, entity_infos):
        count = 0
        with tqdm(total=len(entity_infos)) as pbar:
            pbar.set_description("Processing central node")
            for entity_dict in entity_infos:
                #print('creating central node:',entity_dict['name'])
                node = Node('name', **entity_dict)
                self.g.create(node)
                count +=1
                pbar.update(1)
                #print('central node count:', count)
        return

    '''创建知识图谱实体节点类型schema'''
    def create_graphnodes(self):
        self.create_central_nodes(self.entity_infos)
        for entity in self.entities:
            if entity != 'name':
                print('creating entity node:', entity)
                self.create_node(entity, set(self.entities_dict[entity]))
        return

    '''创建实体关系边'''
    def create_graphrels(self):
        for k,v in self.relations_infos_dict.items():
            self.create_relationship(v[0], v[1], self.relations_dict[k], k, k)
       #self.create_relationship('Disease', 'Food', rels_recommandeat, 'recommand_eat', '推荐食谱')

    '''创建实体关联边'''
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        with tqdm(total=all) as pbar:
            for edge in set(set_edges):
                pbar.set_description("Processing %s edge" % rel_type)
                edge = edge.split('###')
                p = edge[0]
                q = edge[1]
                query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                    start_node, end_node, p, q, rel_type, rel_name)
                try:
                    self.g.run(query)
                    count += 1
                    #print('relation count:', rel_type, count, all)
                    pbar.update(1)
                except Exception as e:
                    print(e)
        return

    '''导出数据'''
    def export_data(self):
        for entity in self.entities:
            f = open('./dict/%s.txt'%entity,'w',encoding='utf-8')

            f.write('\n'.join(list(set(self.entities_dict[entity]))))
            f.close()
            print('Export data finished!')
        return


if __name__ == '__main__':
    backinfo = BackInfo()
    handler = AnyGraph(backinfo.entities,backinfo.infos,backinfo.entities_infos_dict,backinfo.relations_infos_dict)
    print("导出数据中...")
    handler.export_data()
    #exit()
    print("导入图谱节点中...")
    handler.create_graphnodes()
    print("图谱节点导入完成！")
    print("导入图谱边中...")
    handler.create_graphrels()
    print("图谱边导入完成！")
    """
    x = MedicalGraph()
    entities_dict, entity_infos, relations_dict = x.read_nodes_test()
    print(entities_dict)
    print(relations_dict)
    """
