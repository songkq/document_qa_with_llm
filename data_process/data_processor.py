# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: data_processor.py
# @time: 2023/7/22 11:31
from elasticsearch import helpers
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from utils.db_client import milvus_client
from utils.db_client import es_client
from common.baichuan_api import get_text_embedding


# 数据处理
class DataProcessor(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def text_loader(self):
        print(f'loading file: {self.file_path}')
        # 指定要使用的文档加载器
        documents = TextLoader(self.file_path, encoding='utf-8').load()
        return documents

    @staticmethod
    def text_spliter(documents):
        # 接下来，我们将文档拆分成块。
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        return texts

    @staticmethod
    def text_embedding(texts):
        _ids = []
        sources = []
        contents = []
        embeddings = []
        for i, text in enumerate(texts):
            source = text.metadata['source']
            content = text.page_content
            content = content.replace('\n', '')
            embedding = get_text_embedding(content)
            _ids.append(i + 1)
            sources.append(source)
            contents.append(content)
            embeddings.append(embedding)
            print(f'source: {source}, got text {i} embedding...')
        datas = [_ids, sources, contents, embeddings]
        return datas

    @staticmethod
    def es_data_insert(datas):
        if datas:
            action = ({
                "_index": "docs",
                "_type": "_doc",
                "_source": {
                    "source": datas[1][i],
                    "cont_id": datas[0][i],
                    "content": datas[2][i]
                }
            } for i in range(len(datas[0])))
            helpers.bulk(es_client, action)
            print("insert data to es")
        else:
            print("no insert data!")

    @staticmethod
    def milvus_data_insert(datas):
        insert_result = milvus_client.insert(datas)
        milvus_client.flush()
        # 将collection加载至内存
        milvus_client.load()
        print(f"insert data to milvus, {insert_result}")

    def data_insert(self):
        documents = self.text_loader()
        texts = self.text_spliter(documents)
        datas = self.text_embedding(texts)
        self.es_data_insert(datas)
        self.milvus_data_insert(datas)


if __name__ == '__main__':
    DataProcessor(file_path='../files/dengyue.txt').data_insert()
