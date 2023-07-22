# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: baichuan_api.py
# @time: 2023/7/22 15:12
import json
import requests


def get_text_embedding(req_text):
    url = "http://10.241.132.209:8000/v1/embeddings"
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({"model": "Baichuan-13B-Chat", "input": req_text})
    new_req = requests.request("POST", url, headers=headers, data=payload)
    return new_req.json()['data'][0]['embedding']


def chat_completion(message):
    url = "http://10.241.132.209:8000/v1/chat/completions"
    system_role = '你是一个出色的文档问答助手，回答要合理、简洁，回复语言采用中文，。' \
                  '若问题与文本片段相关，请根据给定的文本片段和问题，答案以"根据文档知识"开头' \
                  '若问题与文本片段相关性较小，则使用外部知识回答问题，答案以"根据外部知识"开头。'
    payload = json.dumps({
        "model": "Baichuan-13B-Chat",
        "messages": [
            {
                "role": "system",
                "content": system_role
            },
            {
                "role": "user",
                "content": message
            }
        ]
    })
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()['choices'][0]['message']['content']
