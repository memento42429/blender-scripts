import csv

urllist = {}

urllist.setdefault("a","url1")
urllist.setdefault("a","url2")  # 追加されないことを確認
urllist.setdefault("b","url1")
urllist.setdefault("c","url1")

print(type(urllist))    # ここの型はdict
print(type(urllist["a"]))   # ここの型はstr

with open("url.csv","w",newline='') as f:
    writer = csv.DictWriter(f, fieldnames = ["name","url"])
    writer.writeheader()
    writer.writerows(urllist)

####
# 実行すると
# AttributeError: 'str' object has no attribute 'keys'
# が帰ってきてしまいます。
####