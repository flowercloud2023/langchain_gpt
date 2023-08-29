from pymongo import MongoClient

# 连接到 MongoDB 数据库
client = MongoClient("mongodb://localhost:27017/")
db = client["langchain_DB"]  # 替换为您的数据库名称
collection = db["vector_collection"]  # 替换为您的集合名称

# 定义数据表字段
collection.create_index([("user_input", "text")])  # 创建文本索引以支持文本搜索

# 创建一个空的记录以确保数据表被正确创建
empty_record = {
    "user_input": "",
    "assistant_response": "",
    "vector": []  # 向量字段，存储向量数据，可以为空列表
}

# 插入一个空记录以确保数据表被正确创建
collection.insert_one(empty_record)

# 打印提示信息
print("数据表已创建并插入一个空记录。")

# 示例数据记录，假设您的BERT模型向量维度是768维
example_record = {
    "user_input": "你好，我叫hyp",
    "assistant_response": "你好，Hyp！有什么我可以帮助你的吗？",
    "vector": [0.1] * 768  # 使用实际的向量维度并填充对应的值
}

# 插入示例数据记录
collection.insert_one(example_record)
