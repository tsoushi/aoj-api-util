import json
import logging

import api
import util

logger = logging.getLogger(__name__)

def initLogger(logLevel):
    logLevel = {'debug': logging.DEBUG, 'info': logging.INFO}[logLevel]
    api.logger.setLevel(logLevel)
    logger.setLevel(logLevel)
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logLevel)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    streamHandler.setFormatter(formatter)
    api.logger.addHandler(streamHandler)
    logger.addHandler(streamHandler)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('problem_id', type=str, help='問題ID')
    parser.add_argument('--language', '-l', default=None, help='プログラミング言語')
    parser.add_argument('--out', '-o', type=str, default='out.json', help='出力ファイル名')
    parser.add_argument('--log_level', '-log', choices=['debug', 'info'], default='debug', help='ログ出力レベル')
    parser.add_argument('--status', '-s', type=lambda i:[int(j) for j in i.split(',')], help='「,」区切りで絞り込むstatusを指定する')
    parser.add_argument('--remove-comments', '-rmc', action='store_true', help='コメントを削除する')
    parser.add_argument('--remove-return-tab', '-rmrt', action='store_true', help='改行、タブを削除する')
    parser.add_argument('--normalize', '-n', action='store_true', help='remove-comments、remove-return-tabを行う')
    
    args = parser.parse_args()

    initLogger(args.log_level)

    res = api.Reader.findSubmissionCodesByProblem(
        args.problem_id,
        language=args.language,
        status=args.status
    )

    if args.remove_comments or args.normalize:
        logger.info('remove comments')
        for i in res:
            i[1] = util.removeComments(i[1], i[0]['language'])
        logger.info('remove comments -> done')
    if args.remove_return_tab or args.normalize:
        logger.info('remove return and tab')
        for i in res:
            i[1] = util.removeReturnAndTab(i[1])
        logger.info('remove return and tab -> done')

    if args.out:
        with open(args.out, 'wt', encoding='utf-8') as f:
            f.write(json.dumps(res))
    else:
        print(json.dumps(res))