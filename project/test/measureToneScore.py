# -*- encoding: utf-8 -*-
import os
import pandas as pd
from collections import defaultdict
import csv
from ekonlpy.sentiment import MPCK
mpck = MPCK()
file_list = os.listdir('data/minutes/txt/')
positiveNgram = pd.read_csv('mkt_app_old/positive.csv', sep='\n', header=None, names=['positiveNgram'], encoding='utf-8')
negativeNgram = pd.read_csv('mkt_app_old/negative.csv', sep='\n', header=None, names=['negativeNgram'], encoding='utf-8')

for file in file_list:
    NoOfPositiveNgrams, NoOfnegativeNgrams = 0, 0

    minutes = open('data/minutes/txt/' + file, 'r', encoding='utf-8').read()

    minutesTokens = mpck.tokenize(minutes)
    minutesNgrams = mpck.ngramize(minutesTokens)

    minutesNgramsTotal = minutesNgrams + minutesTokens

    print(file[3:11], '의 ngram 수: ', len(minutesNgramsTotal))
    print(file[3:11], '매칭 결과 : ')

    for mN in minutesNgramsTotal:
        for pN in positiveNgram.positiveNgram:
            if mN == pN:
                NoOfPositiveNgrams = NoOfPositiveNgrams + 1
                break
        #                 print('Positive match ngram: ')
        #                 print(mN, '==', pN)
        for nN in negativeNgram.negativeNgram:
            if mN == nN:
                NoOfnegativeNgrams = NoOfnegativeNgrams + 1
                break
    #                 print('negative match ngram: ')
    #                 print(mN, '==', nN)


    # 감성사전과 매칭되는 ngram이 없는 경우
    if (NoOfPositiveNgrams + NoOfnegativeNgrams) == 0:
        print('매칭되는 ngram 없음 ')
        continue

    print('NoOfPositiveNgrams : ', NoOfPositiveNgrams)
    print('NoOfnegativeNgrams : ', NoOfnegativeNgrams)

    polarityScore_sentence = (NoOfPositiveNgrams - NoOfnegativeNgrams) / (NoOfPositiveNgrams + NoOfnegativeNgrams)

    print('어조지수 : ', polarityScore_sentence)
    print()

    with open('toneScore_newToneScoreGetcode_fromNewsBondDict.csv', 'a', encoding='utf-8') as f:
        f.write(file[3:11] + "," + str(polarityScore_sentence) + '\n')