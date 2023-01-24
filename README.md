# インストール
```
git clone https://github.com/tsoushi/aoj-api-util.git
cd aoj-api-util
python3 -m pip install -r requirements.txt
```

# 使用方法
```
usage: main.py [-h] [--language LANGUAGE] [--out OUT] [--log_level {debug,info}] [--status STATUS] [--remove-comments] problem_id

positional arguments:
  problem_id            問題ID

options:
  -h, --help            show this help message and exit
  --language LANGUAGE, -l LANGUAGE
                        プログラミング言語
  --out OUT, -o OUT     出力ファイル名
  --log_level {debug,info}, -log {debug,info}
                        ログ出力レベル
  --status STATUS, -s STATUS
                        「,」区切りで絞り込むstatusを指定する
  --remove-comments, -rmc
                        コメントを削除する
```
- statusの値
```
# values of submission status
STATE_COMPILEERROR = 0
STATE_WRONGANSWER = 1
STATE_TIMELIMIT = 2
STATE_MEMORYLIMIT = 3
STATE_ACCEPTED = 4
STATE_WAITING = 5
STATE_OUTPUTLIMIT = 6
STATE_RUNTIMEERROR = 7
STATE_PRESENTATIONERROR = 8
STATE_RUNNING = 9
```
引用元：[AOJ API Reference](http://developers.u-aizu.ac.jp/index)

## 例）問題ID`ALDS1_1_A`の正解のC言語のコードをコメントを削除して取得する
```
python3 main.py ALDS1_1_A --language C --status 4 --remove-comments
```