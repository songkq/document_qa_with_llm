本项目用于文档问答，使用向量嵌入 + ES 做召回，再使用LLM做文档问答，Web框架使用Flask。

项目的整体架构如图：

![文档问答流程图](https://percent4.github.io/img/nlp60_5.jpeg)

本项目对应的博客文章：[https://percent4.github.io/2023/07/23/NLP%EF%BC%88%E5%85%AD%E5%8D%81%E4%B8%80%EF%BC%89%E4%BD%BF%E7%94%A8Baichuan-13B-Chat%E6%A8%A1%E5%9E%8B%E6%9E%84%E5%BB%BA%E6%99%BA%E8%83%BD%E6%96%87%E6%A1%A3%E9%97%AE%E7%AD%94%E5%8A%A9%E6%89%8B/](https://percent4.github.io/2023/07/23/NLP%EF%BC%88%E5%85%AD%E5%8D%81%E4%B8%80%EF%BC%89%E4%BD%BF%E7%94%A8Baichuan-13B-Chat%E6%A8%A1%E5%9E%8B%E6%9E%84%E5%BB%BA%E6%99%BA%E8%83%BD%E6%96%87%E6%A1%A3%E9%97%AE%E7%AD%94%E5%8A%A9%E6%89%8B/)

### 启动方式

1. 安装ElasticSearch（版本7.17.0）和Milvus（版本2.2.1），建议使用Docker搭建环境
2. 安装Python第三方模块，参考`requirements.txt`
3. 启动web服务: `python3 server.py`

### 效果测试

> 今年上半年的GDP增长率是多少？
> 
> 根据文档知识，2021年上半年的GDP增长率为5.5%。

> 你知道格里芬的职务吗？
> 
> 格里芬的职务是美国宇航局局长。

> 格里芬发表演说时讲了什么？
> 
> 根据文档知识，格里芬发表演说时讲了如下内容：他认为如果中国人愿意，2020年他们可以实现载人登月工程。此外，叶培建院士也曾发表自己的观点，认为2025年比较合适。然而，根据中国科学院编制的50年长远规划，中国要实现载人登月工程是2030年。

> 日本的国土面积多大？
> 
> \n根据文档知识：日本的国土面积为377,915平方千米。根据外部知识：日本是世界上国土面积第64大的国家，排名在它前面的有俄罗斯、加拿大、美国、中国和澳大利亚等国家。

> 一个地区如果回流生数量多会有什么影响？
> 
> 根据文档知识，一个地区如果回流生数量多可能会对常年在本地上学的学生造成一定的影响，导致学位紧张。但同时，也存在一些家长和学生通过投机行为，试图利用回流生的机会获得更好的教育资源。为了防止这种情况，需要采取措施震慑不法分子。同时，回流生的存在可能对本地学生产生一定的竞争压力，但主要还是要看学生的个人学习表现。

> 今年暑期档电影有哪些？
> 
> 今年暑期档电影市场活跃度持续升温，已有多部电影陆续上映。根据灯塔专业版统计，今年暑期档共有119部新片上映，涵盖了动画、冒险、剧情、儿童、纪录片、惊悚、科幻等多种题材。截至7月22日，暑期档总票房已突破100亿元，预计今年暑期档总票房将在160亿元以上。业内人士预测，今年暑期档有望成为“史上最强暑期档”。

> 封神第一部什么时候上映的？
> 
> 根据文档知识，《封神第一部》于2023年7月20日上映。