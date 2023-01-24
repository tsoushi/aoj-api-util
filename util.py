import re

def removeComments(text: str, language: str):
    if language in ['C', 'C++', 'C++11', 'C++14', 'C++17']:
        return re.sub(r'/\*[\s\S]*?\*/|//.*', '', text)
    raise Exception(f'コメントの削除に対応していない言語です : {language}')