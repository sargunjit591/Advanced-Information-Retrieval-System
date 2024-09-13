
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

with open('inverted_index.pkl', 'rb') as file:
    inverted_index = pickle.load(file)


queries=int(input("Enter the number of queries: "))

def execute_query(query,inverted_index,operations):
    try:
        op1=set(inverted_index[query[0]])
    except:
        return set()
    for i in range (1,len(query)):
        try:
            op2=inverted_index[query[i]]
        except:
            op2=set()
        if operations[i-1]=='AND'or operations[i-1]==' AND':
            result=set(op1).intersection(set(op2))
        elif operations[i-1]=='OR'or operations[i-1]==' OR':
            result=set(op1).union(set(op2))
        elif operations[i-1]=='AND NOT'or operations[i-1]==' AND NOT':
            result=set(op1).intersection(set(inverted_index['I']).difference(set(op2)))
        elif operations[i-1]=='OR NOT'or operations[i-1]==' OR NOT':
            result=set(op1).union(set(inverted_index['I']).difference(set(op2)))
        op1=result
        
    return op1
         


        
for i in range(queries):
    query = input("Enter the query: ")
    query = preprocess_text(query)
    operations=input(f"Enter the operations for query {i+1} (AND, OR, AND NOT, OR NOT) length only {len(query)-1}: ")
    operations = operations.split(',')
    full_query=""
    for i in range(len(query)-1):
        full_query+=query[i]+" "+operations[i]+" "
    full_query+=query[len(query)-1]
    result=execute_query(query,inverted_index,operations)
    print(f"Query {i+1}: {full_query}")
    lol=sorted(result)
    print(f"Number of documents retrieved: {len(result)}")
    print("Documents retrieved: ",lol)
