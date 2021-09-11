# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 22:00:59 2021

@author: takah
"""

import torch
from pytorch_pretrained_bert import BertTokenizer, BertModel

model = BertModel.from_pretrained("C:/Users/takah/Dropbox/My PC (DESKTOP-4MU76QI)/Desktop/卒論用/data/bert/Japanese_L-12_H-768_A-12_E-30_BPE")
bert_tokenizer = BertTokenizer("C:/Users/takah/Dropbox/My PC (DESKTOP-4MU76QI)/Desktop/卒論用/data/bert/Japanese_L-12_H-768_A-12_E-30_BPE/vocab.txt",
                               do_lower_case=False, do_basic_tokenize=False)

# Jumanによるトークナイザ
from pyknp import Juman

class JumanTokenizer():
    def __init__(self):
        self.juman = Juman()

    def tokenize(self, text):
        result = self.juman.analysis(text)
        return [mrph.midasi for mrph in result.mrph_list()]

juman_tokenizer = JumanTokenizer()

text="吾輩は猫である。"
tokens = juman_tokenizer.tokenize(text)
bert_tokens = bert_tokenizer.tokenize(" ".join(tokens))
ids = bert_tokenizer.convert_tokens_to_ids(["[CLS]"] + bert_tokens[:126] + ["[SEP]"])
tokens_tensor = torch.tensor(ids).reshape(1, -1)

