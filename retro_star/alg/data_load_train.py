import pickle
import json
path='dataset/routes_train.pkl' 

# 指定要写入的JSON文件名
file_name = 'train_data.jsonl'
f=open(path,'rb')
data=pickle.load(f)

# print(type(data))
# print(len(data))
# 将数据写入JSON文件
with open(file_name, 'w') as f: 
    for i in range(10):
        json_record = json.dumps(data[i],indent=4)
        f.write(json_record + '\n')





