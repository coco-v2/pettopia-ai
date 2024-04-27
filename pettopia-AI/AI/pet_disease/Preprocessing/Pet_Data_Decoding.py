import pandas as pd

class Pet_Data_Decoding():

    # def __init__(self):

    def data_decoding(self, abn_data:pd.DataFrame, nor_data:pd.DataFrame):

        abn_pet = {}
        nor_pet = {}

        abn_disease_name, abn_CRP, abn_IgG, abn_IL_6, abn_AFP, abn_stree = self.abn_data_decoding(abn_data)
        nor_CRP, nor_IgG, nor_IL_6, nor_AFP, nor_stree = self.nor_data_decoding(nor_data)

        if abn_stree == -1:
            abn_stree = "정보 없음"

        if nor_stree == -1:
            nor_stree = "정보 없음"

        return 0

    def abn_data_decoding(self, abn_data:pd.DataFrame):
        abn_disease_name = abn_data['disease_name']
        abn_CRP = abn_data['CRP']
        abn_IgG = abn_data['IgG']
        abn_IL_6 = abn_data['IL-6']
        abn_AFP = abn_data['AFP']
        abn_stree = abn_data['stress']

        abn_disease_name = abn_disease_name.apply(lambda x: x.split('/') if '/' in x else [x])

        return abn_disease_name, abn_CRP, abn_IgG, abn_IL_6, abn_AFP, abn_stree

    def nor_data_decoding(self, nor_data:pd.DataFrame):
        nor_CRP = nor_data['CRP']
        nor_IgG = nor_data['IgG']
        nor_IL_6 = nor_data['IL-6']
        nor_AFP = nor_data['AFP']
        nor_stree = nor_data['stress']

        return nor_CRP, nor_IgG, nor_IL_6, nor_AFP, nor_stree


