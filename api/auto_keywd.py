import pandas as pd  # dataflame（2次元配列を表で管理できる）を利用するためのライブラリ
import csv
import re
import spacy
import os
import numpy as np
import emoji
from spacy import displacy


########ファイル名の入力#################
#データ名
data_file="tfc001_faq_data_20210605-103313.csv"
#類語辞書名
Synonyms_file="tfc001_synonyms_data_20210607-193550.csv"
#出力名
output_file='出力データ/data_export.csv'
# 「ｗ」は既存のファイルに書き込み、「a」は新規ファイル作成
format_file="w"
##########################################





#CSVを読み込み、二次元配列に入れる
with open(data_file,  encoding="utf-8") as f:
    reader=csv.reader(f) # readerオブジェクトの作成
    text_list = [row for row in reader]

# 最初の一個（カラム名）を削除
text_list.pop(0)
#IDの抜き出しのための、二次元配列を保存
arry_data=[]
for row in range(0,len(text_list)):
    ID_name=text_list[row][4]
    arry_data.append(ID_name)
#print(arry_data)


#「,」の文章内の処理用
for row in range(0,len(text_list)):
    for now in range(0,5):
        text_list[row][now]= text_list[row][now].replace(',', '')




#類語辞書.csvを読み込み、二次元配列に入れる
with open(Synonyms_file,  encoding="utf-8") as f:
    reader=csv.reader(f) # readerオブジェクトの作成
    dictionary_list = [row for row in reader]

#「、」を対象に2次元配列の要素
dictionary_list =[x[0].split(",") for x in dictionary_list ]
#print(dictionary_list)

print('φ(･ｪ･o)~ﾖﾐｺﾐﾁｭｳ・ﾏｴｼｮﾘ')



#print(text_list[0])

#リストを文字列に変換　正規表現での文字列操作の為
text_list = str(text_list)


# メールアドレスを除去
mailad_rej = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
text_list = mailad_rej.sub("", text_list)

# HTMLタグを除去
tag_rej = re.compile(r'<[^>]*?>')
text_list = tag_rej.sub("", text_list)

#URL除去
url_rej = re.compile(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+')
text_list = url_rej.sub("", text_list)

"""
#空白、改行除去
spc_rej = re.compile(r'[\s \u3000 \t \n]')
text_list = spc_rej.sub("", text_list)
"""
#絵文字の除去 
text_list  = ''.join(['' if c in emoji.UNICODE_EMOJI else c for c in text_list])

#記号除去
code_rej = re.compile('[!"#$%&\'\\\\()*+\\-./:;<=>?@[\\]^_`{|}~〔〕“”〈〉『』【】＆＊・（）＄＃＠？！｀＋￥％]')
text_list = code_rej.sub("", text_list)
#print(text_list)




#リスト型に戻す
text_list = text_list.split(',')
print(len(text_list))


# ↓これは何故か1文字毎にリスト変換される謎 使えない。日本語だと使えない？
# text_list = list(text_list)

#↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓GiNZAの処理↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

nlp = spacy.load('ja_ginza')

#抽出する品詞
select_conditions = '名詞'

#英単語2文字除去の対象外設定正規表現を外部ファイルから作る
f1 = open('2文字でも残すアルファベット.txt', 'r' ,encoding="utf-8")
exp1 = 'r\'^(?!.*' + '|'.join(f1) + ').*(?=^[a-zA-Z]{2}).*$\''
exp1 = exp1.replace('\n','')
#print(exp1)

#無意味なキーワードを削除する規表現を外部ファイルから作る
f2 = open('除外キーワード.txt', 'r' ,encoding="utf-8")
exp2 = '^' + '$|^'.join(f2) + '$'
exp2 = exp2.replace('\n','')
#print(exp2)

#処理を関数名kywdにまとめて、動かせるようにする
def kywd(item):
    #print('hall')
    #print(item)
    doc = nlp(item)

    words_pos = []
    for sent in doc.sents:
        for token in sent:
            condition = token.tag_
            condition = condition.split('-')[0]
            # 品詞が名詞　且つ　2文字以上であれば、配列に加える
            if condition == select_conditions and len(token) != 1:
                token = str(token)
                #exp1で設定した以外の2文字のアルファベットを正規表現で除去
                alpha2_rej = re.compile(exp1)
                token = alpha2_rej.sub("", token)
                #exp2で設定した無意味なキーワードを正規表現で除去
                garbage_rej = re.compile(exp2)
                token = garbage_rej.sub("", token)
                if token != '':
                    words_pos.append(token)

    #words_posをテキストのリストに変換
    words_pos = [str(i) for i in words_pos]
    #print(words_pos)

    #リストを改行して結合
    text_result = '\n'.join(words_pos)
    return text_result

#↑↑↑↑↑↑↑↑↑↑↑↑↑↑GiNZAの処理↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

#GiNZAよ走れ
print('ｳｫｵｫｫｫｱｧｵｱｱｱｧｱｧｧ(*・`д・)ｶｲｾｷﾁｭｳ')
#形態素分析を行い、名詞を取り出す
newList = [kywd(item) for item in text_list]
print(len(newList))


#類語辞書分カウント
count_1=0
#1行毎の類語分カウント
count_2=0
#入力データ分カウント
count_3=0
#IDをカウントで取得
count_4=0
#類語を入れる配列
Synonyms=[]
#IDを入れる配列
ID=[]

ceak=[]

#マッチング処理
print("マッチング始めるよ")
#入力データ分だけ繰り返す(5項目×Id数)
for w in newList:
    #newList[count_3]の位置がIDの場合
    if count_3%5==0:
      count_4+=1
    #類語辞書の数だけ繰り返す
    for b in dictionary_list:
        #1行毎の類語だけ繰り返す
        for t in dictionary_list[count_1]:
            #if()
            #マッチングした場合、ID・類語取得
            if dictionary_list[count_1][count_2] in newList[count_3]:
                #IDの取得
                ID.append(arry_data[count_4-1])
                #print(ID)
                #リストを文字列に変換
                s=' '.join(dictionary_list[count_1])
                #print(s)
                #類語を取得
                Synonyms.append(s)
                ceak.append(newList[count_3])
                #print(Synonyms)
                #マッチング内容確認
                #print(newList[count_3])
                #print(dictionary_list[count_1][count_2])
            count_2+=1
        count_2=0
        count_1+=1
    count_1=0
    count_3+=1
print("終了")
#取得したい内容の確認用
#print(len(ID))
#print(ceak[1])
#print(Synonyms[1])

#２次元配列でIDと類語の紐付け
test=[]
for row in range(0,len(Synonyms)): 
     test.append(([ID[row], Synonyms[row]]))
#２次元配列でIDと類語のセットの重複を消す
result = []
for line in test:
    if line not in result:
        result.append(line)

#Pythonでリストの辞書を使って、一致しているIDの類語の追加
id_dict = {}
ba=[]
for d in result:
    id_dict.setdefault(d[0],[]).append(d[1])
#print(id_dict)
#辞書から類語の抜き出し
for i, l in id_dict.items():
   # print(i, " : ", sorted(l))
    ba.append(' '.join(sorted(l)))

#IDの重複を消す)
ID = list(dict.fromkeys(ID))



output_data=[]
#２次元配列でIDと類語の紐付け
for row in range(0,len(ba)): 
     output_data.append(([ID[row], ba[row]]))
#print(output_data)

print("類語データ："+str(len(output_data)))
print("新規ファイル作成数:"+str((len(output_data)//99)))
#ファイルの個数
file_count=-1
#書き込む数のカウント
line_count=0
#99で割り切った数
lengeh=len(output_data)//99
#print(lengeh)



print("書き込み開始")
for neo in range(0,lengeh+1):
    file_count+=1
    file_name='出力データ/data_export'+str(file_count)+'.csv'
    #最初に既存のデータに書き込み
    if file_count==0:
        #csvに書き込み
        # 「ｗ」は書き込み、「a」はファイル作成
        with open(output_file,format_file,encoding="utf-8")as f:
            writer = csv.writer(f,lineterminator='\n')
            writer.writerow(['dicID', 'DictionaryData'])
            for row in range(0,99):
                 writer.writerow(output_data[row])
                 line_count+=1
                 output_data.pop(0)
            print(line_count)
    #余りの書き込み
    elif file_count==lengeh:
        with open(file_name,"a",encoding="utf-8")as f:
            writer = csv.writer(f,lineterminator='\n')
            writer.writerow(['dicID', 'DictionaryData'])
            for row in range(0,len(output_data)):
                 writer.writerow(output_data[0])
                 line_count+=1
                 output_data.pop(0)    
            print("ラスト")  
            print(line_count)
    #99で割り切る数だけ書き込み
    else:
        with open(file_name,"a",encoding="utf-8")as f:
            writer = csv.writer(f,lineterminator='\n')
            writer.writerow(['dicID', 'DictionaryData'])
            for row in range(0,99):
                writer.writerow(output_data[0])
                line_count+=1
                output_data.pop(0)
            print(line_count)
    print(file_count)
print("書き込み終了")
