#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2021/2/20 上午11:52
# @File    : phoneModel.py
# @Software: PyCharm

import os, re
import pandas as pd


class PhoneModel:
    def __init__(self, origin=1):
        # 获取所有的品牌名
        self.brands = [brand for brand in os.listdir(os.path.join(repo_path, 'brands')) if brand.endswith('md')]

    def get_model(self, brand):
        """读取原始数据"""
        with open(os.path.join(repo_path, 'brands', brand), 'rt',encoding='utf-8') as file:
            brand_info = file.read()
        brand_info_list = [item for item in brand_info.split('\n') if re.match('`.+: ', item) is not None]

        model_df = pd.DataFrame(columns=['brand', 'model', 'area', 'brand_name', 'model_name'])
        for record in brand_info_list:
            record_list = record.replace('`', '').split(':')
            if record_list[1] == '**':
                continue
            model_str = record_list[0].replace(brand[:-3].split('_')[0].upper(), '').strip()
            model_list = [x for x in model_str.split() if x not in ('SHARK', 'HUAWEI', 'Letv', 'Le', 'ONE')]
            head = model_list[0][:3]
            tail = model_list[0][-3:]
            if all([x.startswith(head) or x.endswith(tail) or x.find('-') > 0 for x in model_list]):
                for model in model_list:
                    model_df.loc[len(model_df)] = (
                    brand[:-3].split('_')[0], model, 'en' if brand.find('_en') > 0 else 'cn',
                    brand_map.get(brand[:-3].split('_')[0], '其他'), record_list[1])
        return model_df

    def get_all(self):
        brand_model = pd.DataFrame(columns=['brand', 'model', 'area', 'brand_name', 'model_name'])

        for brand in self.brands:
            print('processing', brand)
            self.get_model(brand)
            brand_model = brand_model.append(self.get_model(brand))
        brand_model.model_name = brand_model.model_name.apply(lambda x:str(x).strip().replace('"',''))
        self.brand_model = brand_model.reset_index(drop=True).drop_duplicates().reset_index(drop=True)

    def data_save(self):
        project_path = os.path.dirname(os.path.realpath(__file__))
        self.brand_model.to_csv(os.path.join(project_path, 'brand_model.csv'), index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    repo_path = '.'
    brand_map = {'meizu': '魅族', 'smartisan': '锤子', 'vivo': 'VIVO', 'realme': 'REALME',
                 'xiaomi': '小米', 'apple': '苹果', 'oppo': 'OPPO', 'nokia': '诺基亚',
                 'mitv': '小米电视', 'huawei': '华为', 'oneplus': '一加', 'motorola': '摩托罗拉',
                 'samsung': '三星', 'zte': '中兴', 'letv': '乐视', 'honor': '荣耀', 'lenovo': '联想',
                 '360shouji': '奇酷', 'nubia': '努比亚'}

    pm = PhoneModel()  # 初始 pm=PhoneModel(0),后续更新可不填
    pm.get_all()
    pm.data_save()
