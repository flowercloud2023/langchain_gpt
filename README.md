# langchain_gpt

langchain_gpt_1.py
使用LangChain框架和MongoDB数据库，创建一个基于GPT的聊天机器人，同时记录聊天历史并判断用户基本信息。主要功能：

连接到 MongoDB 数据库：通过指定连接字符串，连接到 MongoDB 数据库。

创建聊天模型：使用ChatOpenAI创建一个聊天模型，其中包括使用API​​密钥。

创建聊天提示模板：创建ChatPromptTemplate，设置系统消息和用户消息的模板，用于构建聊天对话。

创建链：使用 LLMChain 创建聊天链，将聊天模型、聊天提示模板等参数作为参数。

聊天循环：在无限循环中，用户可以输入消息，然后聊天链会根据输入生成机器人回复。

从数据库读取聊天历史：在每次循环中，代码会从 MongoDB 数据库中读取之前的聊天历史。

构建输入：根据之前的聊天历史和当前用户输入，构建输入文本。

运行聊天模型：使用链来运行聊天模型，生成机器人回复。

输出机器人回复：打印输出机器人的回复。

存储聊天历史：将用户输入和机器人回复存储到 MongoDB 数据库的 ChatHistory 集合中。

所使用的框架和库：

LangChain：一个用于创建聊天机器人的Python框架，支持构建聊天链、添加记忆等功能。

ChatOpenAI：LangChain提供聊天模型，用于生成机器人的回复。

ChatPromptTemplate：用于构建聊天提示模板，指定系统消息和用户消息的模板。

LLMChain：构建聊天链的核心组件，将聊天模型、提示模板等结合起来。

MongoDB：一个流行的NoSQL数据库，用于存储聊天历史和用户信息。

pymongo：用于Python与MongoDB交互的库，包括连接数据库、插入数据等操作。

通过这些框架和库的结合使用，您可以创建一个能够与用户进行聊天、记录历史并判断用户信息的聊天机器人应用。

表：

[ { "user_id": "", "聊天": [ { "时间戳": "", "user_input": "", "assistant_response": "" } ] } ]

在这个JSON中，user_id是一个字段，代表用户的唯一标识。chats是一个仓库，每个元素代表一次聊天记录，包含计时器、用户输入和助手回复字段。可以根据需求进行扩展和修改，添加更多多字段或修改字段的结构。




![c8dd1465e8885ed414969db5fb7f569](https://github.com/flowercloud2023/langchain_gpt/assets/55479839/f24fc36e-6641-4c2a-91af-556f1d776d79)






langchain_gpt_2.py
更新langchain_gpt_1.py

交互式聊天系统，使用了以下框架和组件：

MongoDB：作为用于存储聊天记录和提供数据的数据库。

ChatOpenAI：一个用于处理自然语言生成的库，用于创建聊天模型，即助手。通过调用OpenAI API来生成机器人的回复。

LLMChain：一个链式模型，用于根据聊天模板和聊天模型生成对话回复。这里的聊天模型是通过 OpenAI 的 API 进行调用的。

BertTokenizer 和 BertModel：这些是 Hugging Face Transformers 库中的工具，用于将文本输入编码为 BERT 模型可以处理的格式，并从 BERT 模型中获取文本的支撑表示。

Sklearn：使用Sklearn库中的cosine_similarity函数来计算支持之间的余弦相似度。

功能概要：

连接到 MongoDB 数据库，创建一个用于存储聊天记录和数据处理的集合。

创建一个聊天模型，使用OpenAI API进行回复生成。

创建聊天提示模板，定义系统和用户消息的格式。

创建LLMChain，将聊天模型和聊天提示模板组合成链式模型。

加载预训练的BERT模型和分词器用于文本支持化。

在聊天循环中，用户获取输入，并使用 BERT 获取输入的表示。

查询数据库中的支撑记录，计算用户输入支撑与支撑记录之间的余弦相似度，找到相似度最高的匹配。

如果找到匹配的聊天记录，会将匹配的聊天记录和用户当前输入一起作为提示，调用LLMChain生成回复。

如果没有匹配的聊天记录，直接使用用户输入调用LLMChain生成回复。

输出机器人的回复，把用户输入和机器人回复到数据库中。

Becode实现了一个基于聊天记录和支持相似度的聊天系统，旨在通过提供更相关的回复来增强用户体验。

表：见model.py


![875697660c4c6ec4d31a759b44ad8b5](https://github.com/flowercloud2023/langchain_gpt/assets/55479839/22393389-dcb0-4930-9f24-28e14fd938f6)


