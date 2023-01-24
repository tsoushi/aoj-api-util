import re

def removeComments(text: str, language: str):
    if language == 'C':
        return re.sub(r'/\*[\s\S]*?\*/|//.*', '', text)
    raise Exception(f'コメントの削除に対応していない言語です : {language}')