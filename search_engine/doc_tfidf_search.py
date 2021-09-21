from sklearn.feature_extraction.text import TfidfVectorizer
import json
import pandas as pd
import re
import numpy as np

def clean_data(doc):
    res = doc.replace("/", " ").replace("（", "").replace("／", "").replace("）", "").replace("」", "").replace("「", "")
    res = re.sub(r'[0-9]', '', res)
    return res

def get_similar_articles(q, df):
    print("query:", q)
    print("查詢結果: ")
    # Convert the query become a vector
    q = [q]
    q_vec = vectorizer.transform(q).toarray().reshape(df.shape[0],)
    sim = {}
    # Calculate the similarity
    lens = df.shape[1]
    for i in range(lens):
        sim[i] = np.dot(df.loc[:, i].values, q_vec) / np.linalg.norm(df.loc[:, i]) * np.linalg.norm(q_vec)
    
    # Sort the values 
    sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)
    
    return sim_sorted

def doc_vectorizer(docs):
    # vectorize the documents
    X = vectorizer.fit_transform(docs).T.toarray()
    df = pd.DataFrame(X, index=vectorizer.get_feature_names())    
    return df


def write_result(corpus):
    with open("result.txt", "w") as f:
        for content in corpus:
            content += "\n"
            f.write(content)


if __name__ == "__main__":
    with open("/home/labpc1/Documents/Project/dobby/dataset/ioh1500_arti.json") as f:
        content = json.load(f)

    documents = []
    vectorizer = TfidfVectorizer()
    # corpus preprocess

    for doc in content:
        try:
            sents = doc['arti']['result_segmentation']
            sents = clean_data(sents)
            documents.append(sents)
        except Exception as e:
            # documents.append("的")
            pass

    doc_vec = doc_vectorizer(documents)

    not_end = True
    keywords = []
    # corpus_pre = documents
    while(not_end):
        res_dict = {}
        q = input("keyword:")
        keywords.append(q)
        sim_sorted = get_similar_articles(q, doc_vec)
        print(keywords)


        query_lens = 0
        corpus = []
        for k, v in sim_sorted:
            if v != 0.0:
                query_lens += 1
                # print(len(corpus_pre))
                content = documents[k].replace(" ", "")
                corpus.append(content)
                summary = corpus[-1]
        
        res_dict[q] = corpus        
        print(query_lens)

        final_len = []

        if query_lens < 3:
            print(keywords)
            print(f"你想要的內容應該在這{query_lens}篇中")
            # print(corpus)
            write_result(corpus)
            not_end = False
        else:
            doc_vec = doc_vectorizer(corpus)