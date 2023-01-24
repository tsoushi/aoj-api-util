import zipfile
import os
import json
import logging

import requests

logger = logging.getLogger(__name__)

API_ENDPOINT = 'https://judgeapi.u-aizu.ac.jp'

class AOJAPI:
    @staticmethod
    def pageLoad(uri):
        logger.debug(f'call AOJ API : {uri}')
        page = 0
        size = 10000
        results = []
        while 1:
            uriFormatted = uri.format(page=page, size=size)
            logger.debug(f'request: {uriFormatted}')
            res = requests.get(uriFormatted)
            data = json.loads(res.content)
            results.extend(data)
            if len(data) < size:
                logger.debug(f'call AOJ API -> complete : {len(results)} contents')
                return results
            page += 1

    @staticmethod
    def findSolutionsByProblem(problemId, language=None):
        uri = API_ENDPOINT + '/solutions/problems/' + problemId + '?page={page}&size={size}'
        if language:
            uri = API_ENDPOINT + '/solutions/problems/' + problemId + '/lang/' + language + '?page={page}&size={size}'
        return AOJAPI.pageLoad(uri)
    
    @staticmethod
    def findSubmissionByProblem(problemId, language=None):
        uri = API_ENDPOINT + f'/submission_records/problems/{problemId}' + '?page={page}&size={size}'
        res = AOJAPI.pageLoad(uri)
        if language:
            res = [i for i in res if i['language'] == language]
        return res

class Reader:
    sourcePath = './source'

    @staticmethod
    def getCodeByIds(judgeIds: list, toIdFunc=None):
        return Reader._getCodeByIds(Reader.sourcePath, judgeIds, toIdFunc)

    @staticmethod
    def findCodesByProblem(problemId, language=None):
        solutions = AOJAPI.findSolutionsByProblem(problemId, language)
        return Reader.getCodeByIds(solutions, lambda i:i['judgeId'])
    
    @staticmethod
    def findSubmissionCodesByProblem(problemId, language=None):
        submissions = AOJAPI.findSubmissionByProblem(problemId, language)
        return Reader.getCodeByIds(submissions, lambda i:i['judgeId'])
    
    @staticmethod
    def _getCodeByIds(sourcePath: str, judgeIds: list, toIdFunc=None):
        if toIdFunc == None:
            toIdFunc = lambda i: i
        judgeIds = sorted(judgeIds, key=toIdFunc)
        codes = []
        currentZipIndex = -1
        zipF = None
        fileFoundCount = 0

        logger.debug('extract codes')
        for i, judgeId in enumerate(judgeIds):
            print(f'{i} / {len(judgeIds)}' + ' '*10, end='\r')
            targetZipIndex = int(toIdFunc(judgeId) / 100000)
            if targetZipIndex != currentZipIndex:
                if zipF != None:
                    zipF.close()
                currentZipIndex = targetZipIndex
                try:
                    zipF = zipfile.ZipFile(sourcePath + os.sep + str(currentZipIndex).zfill(3) + '.zip')
                except FileNotFoundError:
                    break
            try:
                fileName = str(currentZipIndex).zfill(3) + f'/{toIdFunc(judgeId)}.txt'
                with zipF.open(fileName) as f:
                    codes.append([judgeId, f.read().decode('utf-8')])
                    fileFoundCount += 1
            except KeyError:
                pass
        if zipF != None:
            zipF.close()
        logger.debug(f'extract codes -> complete : {fileFoundCount}/{len(judgeIds)} codes was found')
        return codes