import torch
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.chains import LLMChain
from pymongo import MongoClient
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 连接到 MongoDB 数据库
client = MongoClient("mongodb://localhost:27017/")
db = client["langchain_DB"]  # 替换为您的数据库名称
collection = db["vector_collection"]  # 替换为您的集合名称

# 创建聊天模型
chat_model = ChatOpenAI(openai_api_key='')

# 创建聊天提示模板
chat_template = ChatPromptTemplate.from_messages([
    ("system", "你好！我是智能助手。"),
    ("human", "{user_input}"),
])

# 创建链
chain = LLMChain(
    llm=chat_model,
    prompt=chat_template
)

# 加载预训练的BERT模型和tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
bert_model = BertModel.from_pretrained('bert-base-chinese')

# 聊天循环
while True:
    user_input = input("用户: ")  # 用户输入

    # 使用tokenizer将用户输入转换为token
    input_tokens = tokenizer.encode(user_input, add_special_tokens=True)
    input_tokens = torch.tensor(input_tokens).unsqueeze(0)  # 添加batch维度

    # 使用BERT模型获取用户输入的向量表示
    with torch.no_grad():
        outputs = bert_model(input_tokens)
        user_input_vector = outputs.last_hidden_state.mean(dim=1).squeeze()  # 取平均得到文本向量

    # 查询匹配的向量记录
    cursor = collection.find({"vector": {"$exists": True}})  # 获取所有包含 "vector" 字段的记录
    best_match = None
    best_similarity = -1

    for record in cursor:
        vector = np.array(record.get("vector", []))  # 获取向量数组，如果不存在则默认为空列表
        if vector.size == 0:
            continue  # 如果向量数组为空，则跳过余弦相似度计算

        similarity = cosine_similarity([user_input_vector], [vector])[0][0]

        if similarity > best_similarity:
            best_similarity = similarity
            best_match = record

    if best_match:
        matched_chat = best_match["user_input"]

        # 使用匹配的聊天记录和用户当前输入作为提示，获取GPT回复
        response = chain.run({"user_input": f"{matched_chat}\n用户: {user_input}"})
    else:
        # 未找到匹配的聊天记录，直接使用用户输入
        response = chain.run({"user_input": user_input})

    # 输出机器人的回复
    print("助手:", response)

    # 将用户输入和助手回复存储到数据库中
    chat_history_entry = {
        "user_input": user_input,
        "assistant_response": response,
    }
    collection.insert_one(chat_history_entry)
