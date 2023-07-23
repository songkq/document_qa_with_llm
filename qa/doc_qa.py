# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: doc_qa.py
# @time: 2023/7/22 14:06
from utils.db_client import es_client, milvus_client
from data_process.data_processor import get_text_embedding
from common.baichuan_api import chat_completion


# 文档问答
class DocQA(object):
    def __init__(self, query):
        self.query = query

    def get_milvus_search_result(self):
        # milvus search content
        vectors_to_search = [get_text_embedding(self.query)]
        # 通过嵌入向量相似度获取相似文本，数量为3个
        search_params = {
            "metric_type": "IP",
            "params": {"nprobe": 10},
        }
        result = milvus_client.search(vectors_to_search, "embeddings", search_params, limit=2, output_fields=["text"])
        return [_.entity.get('text') for _ in result[0]]

    def get_es_search_result(self):
        result = []
        # 查询数据(全文搜索)
        dsl = {
            'query': {
                'match': {
                    'content': self.query
                }
            },
            "size": 2
        }
        search_result = es_client.search(index='docs', body=dsl)
        if search_result['hits']['hits']:
            result = [_['_source']['content'] for _ in search_result['hits']['hits']]
        return result

    def get_context(self):
        contents = []
        # 去重
        milvus_search_result = self.get_milvus_search_result()
        es_search_result = self.get_es_search_result()
        for content in milvus_search_result + es_search_result:
            if content not in contents:
                contents.append(content)
        return contents

    def get_qa_prompt(self):
        # 建立prompt
        prefix = f"使用下面的文本片段列表，回答问题：{self.query}\n\n"
        context = []
        for i, text in enumerate(self.get_context()):
            context.append(f"文本片段{i+1}: {text}\n")
        qa_chain_prompt = prefix + ''.join(context)
        print(qa_chain_prompt)
        return qa_chain_prompt

    def answer(self):
        message = self.get_qa_prompt()
        result = chat_completion(message)
        return result


if __name__ == '__main__':
    question = '美国人什么时候登上月球的？'
    question = '戚发轫的职务是什么？'
    # question = '你知道格里芬的职务吗？'
    # question = '格里芬发表演说时讲了什么？'
    question = '日本的面积有多大？'
    reply = DocQA(question).answer()
    print(reply)

