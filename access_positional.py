

import os
import string
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
def preprocess_text(text):
    # Lowercase the text
    text = text.lower()

    # Tokenization
    tokens = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]

    # Remove punctuations
    tokens = [token for token in tokens if token not in string.punctuation]

    # Remove blank space tokens
    tokens = [token for token in tokens if token.isalnum()]

    return tokens

with open('positional_index.pkl', 'rb') as file:
    positional_index = pickle.load(file)


queries=int(input("Enter the number of queries: "))

def execute_query(query,positional_index):
    answer=set()
    dataset_path='text_files'
    try: 
        op1=positional_index[query[0]]
    except:
        return answer
    for filename,positions in op1:
        file_path = os.path.join(dataset_path, filename)
        with open(file_path, 'r') as file:
            text = file.read()
            tokens=text.split()
        flag=True
        if positions+len(query)>len(tokens):
            flag=False
        else:
            for i in range(positions+1,positions+len(query)):
                if tokens[i]!=query[i-positions]:
                    flag=False
                    break

        if flag==True:
            answer.add(filename)


    return answer
         


        
for i in range(queries):
    query = input("Enter the query: ")
    query = preprocess_text(query)
    result=execute_query(query,positional_index)

    lol=sorted(result)
    print(f"Number of documents retrieved: {len(result)}")
    print("Documents retrieved: ",lol)

