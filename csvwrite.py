import csv
 
# ヘッダー
header = ['ID', 'name']
 
# 内容
body = [
  [0, 'Alex'],
  [1, 'John'],
  [2, 'Bob']
]

forcsv = []

for cont in body[0]:
    forcsv.append(body)

# ファイルを書き込みモードでオープン
with open('sample.csv', 'w') as f:
 
  writer = csv.writer(f)  # writerオブジェクトを作成
  writer.writerow(header) # ヘッダーを書き込む
  writer.writerows(forcsv)  # 内容を書き込む