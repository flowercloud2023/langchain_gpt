from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.chains import LLMChain
from pymongo import MongoClient

# 连接到 MongoDB 数据库
client = MongoClient("mongodb://localhost:27017/")  # 替换为您的 MongoDB 连接字符串
db = client["langchain_DB"]  # 使用数据库名 langchain_DB
collection = db["ChatHistory"]  # 使用集合名 ChatHistory

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

# 聊天循环
while True:
    user_input = input("用户: ")  # 用户输入

    # 从数据库读取聊天历史
    user_memory = collection.find()

    # 构建聊天历史字符串
    chat_history = ""
    for chat_entry in user_memory:
        if "user_input" in chat_entry and "assistant_response" in chat_entry:
            chat_history += f"用户: {chat_entry['user_input']}\n"
            chat_history += f"助手: {chat_entry['assistant_response']}\n"

    # 构建输入，包括以前的聊天历史和当前用户输入
    input_text = f"{chat_history}用户: {user_input}\n"

    # 运行聊天模型
    response = chain.run({"user_input": input_text})

    # 输出机器人的回复
    print("助手:", response)

    # 将用户输入和助手回复存储到数据库中
    chat_history_entry = {
        "user_input": user_input,
        "assistant_response": response,
    }
    collection.insert_one(chat_history_entry)
