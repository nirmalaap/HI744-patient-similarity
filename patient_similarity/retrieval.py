import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi

def build_tfidf(texts, max_features=None):
    v=TfidfVectorizer(lowercase=False, token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z]+\b",
        smooth_idf=True, sublinear_tf=True, norm="l2", max_features=max_features,
        dtype=np.float32)
    return v.fit_transform(texts), v

def build_bm25(texts):
    return BM25Okapi([x.split() for x in texts], k1=1.5, b=0.75)

def _top(scores, self_index, uids, k):
    scores[self_index]=-np.inf
    count=min(k, max(0,len(uids)-1))
    ix=np.argpartition(scores,-count)[-count:] if count else []
    return [uids[j] for j in sorted(ix,key=lambda j:scores[j],reverse=True)]

def retrieve_tfidf(matrix,uids,k=5):
    result={}
    for start in range(0,len(uids),128):
        sims=cosine_similarity(matrix[start:start+128],matrix)
        for off,row in enumerate(sims):
            i=start+off
            result[uids[i]]=_top(row,i,uids,k)
    return result

def retrieve_bm25(model,texts,uids,k=5):
    docs=[x.split() for x in texts]
    return {uid:_top(np.asarray(model.get_scores(docs[i]),dtype=float),i,uids,k)
            for i,uid in enumerate(uids)}
