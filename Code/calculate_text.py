# distinct_count/all data*100>threshold -> non categorical
# threshold=70
# 키워드는 distinct value와 다름, distinct value는 칼럼 하나!=단어, 그러면 distinct value가 필요한가?
# 키워드를 distinct value를 가지고 뽑아내는 방식이 좀 더 효율적?
#
# 일단 키워드도 저장
#
#

import pandas as pd
import gensim
from gensim import corpora
from nltk.corpus import stopwords
from nltk import word_tokenize
import nltk
import konlpy
from soynlp.noun import NewsNounExtractor
from soynlp.noun import LRNounExtractor_v2


def main(col_name, dic): #df=calculate_similarity에서 tmp(dict type)
    try:
        # nltk.download('punkt')
        # nltk.download('wordnet')
        # nltk.download('stopwords')
        print(dic)
        data = pd.read_csv('korea_stopwords.csv', encoding='utf-8')
        df = pd.DataFrame(data)
        ko_stop_words = set(df['stopwords'])
        wlem = nltk.WordNetLemmatizer()
        ko_one_word = ['감', '값', '검', '곰', '공', '괌', '관', '군', '국', '굴', '굿', '궁', '궐', '귤', '글', '금', '껌', '꽃', '꿈',
                       '꿩', '끈',
                       '낫', '낮', '넋', '놋', '늪', '달', '닭', '담', '댐', '덤', '돌', '돔', '돛', '둑', '땀', '땅', '뜰',
                       '룰', '립', '링', '맛', '말', '멋', '면', '몫', '못', '뭍', '밥', '밤', '뱀', '배', '벌', '범', '벗', '벼', '벽',
                       '병', '볕', '봄', '복', '봉',
                       '빗', '비', '빚', '빛', '삯', '산', '삵', '삶', '삽', '새', '셈', '설', '성', '솥', '솜', '쇠', '숨', '숲', '숯',
                       '슛',
                       '쌀', '쌈', '쌍', '썰', '쑥', '앎', '연', '엿', '옷', '옻', '왕', '웍', '육', '윷', '잼', '쟁', '잣', '잠', '전',
                       '죽', '쥐', '집', '짚', '짝',
                       '책', '창', '천', '철', '첩', '체', '칡', '침', '캔', '칼', '칸', '캠', '콩', '톱', '팥', '팬', '폐', '폰', '폼',
                       '품', '풀'
                            '학', '햄', '핵', '흙', '힘']
        stop_word=set(stopwords.words('english'))

        df=pd.DataFrame(columns=[col_name])
        df[col_name]=list(dic.keys())
        df[col_name] = df[col_name].str.replace("[^a-zA-Zㄱ-힣0-9]", " ")
        df[col_name] = df[col_name].astype('str')

        noun_extractor = NewsNounExtractor(verbose=False)
        noun_extractor.train(df[col_name].to_list())
        nouns = noun_extractor.extract()
        n_list = [x[0] for x in nouns.items() if len(x[0])>1]
        n_list = [x for x in n_list if len(x) > 2 or (len(x) == 1 and x in ko_one_word)]
        kor = df[col_name].apply(lambda x: [item for item in n_list if item in x])

        eng = df[col_name].str.replace("[^a-zA-Z0-9]", " ")
        eng = eng.apply(lambda x: x.lower())
        eng = eng.apply(lambda x: word_tokenize(x))
        eng = eng.apply(lambda x: [wlem.lemmatize(item) for item in x])
        eng = eng.apply(lambda x: [item for item in x if item not in stop_word and len(item) > 2])
        result = kor+eng

        keyword = []
        try:
            dictionary = corpora.Dictionary(result)
            corpus = [dictionary.doc2bow(text) for text in result]
            ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=1, id2word=dictionary, passes=15)  # passes=알고리즘 동작횟수
            topics = ldamodel.top_topics(corpus, topn=30)
            for item in topics[0][0]:
                keyword.append(item[1])
        except:
            pass
        return keyword
    except AttributeError:
        pass
