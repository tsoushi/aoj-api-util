import json
import logging

import api

def initLogger(logLevel):
    logLevel = {'debug': logging.DEBUG, 'info': logging.INFO}[logLevel]
    api.logger.setLevel(logLevel)
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logLevel)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    streamHandler.setFormatter(formatter)
    api.logger.addHandler(streamHandler)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('problem_id', type=str, help='問題ID')
    parser.add_argument('--language', '-l', default=None, help='プログラミング言語')
    parser.add_argument('--out', '-o', type=str, default='out.json', help='出力ファイル名')
    parser.add_argument('--log_level', '-log', choices=['debug', 'info'], default='info', help='ログ出力レベル')
    args = parser.parse_args()

    initLogger(args.log_level)

    res = api.Reader.findSubmissionCodesByProblem(args.problem_id, args.language)

    if args.out:
        with open(args.out, 'wt', encoding='utf-8') as f:
            f.write(json.dumps(res))
    else:
        print(json.dumps(res))