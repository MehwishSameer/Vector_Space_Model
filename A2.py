import re
import nltk
from nltk.stem import PorterStemmer
import math
nltk.download('punkt')

"""### **Data Preprocessing:**"""

def clean(term):
    ps = PorterStemmer()
    term = term.lower()
    term = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", term) #Remove Unicode
    term = re.sub(r'[^\w\s]','',term)
    term = ps.stem(term)
    return term


stop = []
with open('Stopword-List.txt', 'r') as f:
    for x in f:
        stop += x.split()

print(sorted(stop))


def stopwords_removal(x):
    line_without_stop = [word for word in nltk.word_tokenize(x) if not word in stop]
    return line_without_stop


def stopwords_removal_words(x):
    if not x in stop:
        return False
    else:
        return True


docs_tokenize = []
for i in range(1, 31):
    # print(i)
    temp_doc = []
    with open("Dataset/" + str(i) + ".txt", "r") as file:
        file = file.read().replace(".", "").replace("n't", " not").replace("'", "").replace("]", " ").replace("[", "").replace( ",", " ").replace("?", "").replace("\n", " ").replace("-", " ").replace('/', " ")
        for line in file.split("."):
            line = stopwords_removal(line)
            for word in line:
                word = clean(word)
                if word != "":
                    temp_doc.append(word)
        docs_tokenize.append(temp_doc)


"""### **Positional Index:**"""
tokens = []
positional={}
for i in range(1,31):
  with open('Dataset/'+str(i)+'.txt', 'r') as f:
    f = f.read().replace(".","").replace("n't"," not").replace("'","").replace("]"," ").replace("[","").replace(","," ").replace("?","").replace("\n"," ").replace("-"," ").replace('/'," ")
    pos=-1
    for word in nltk.word_tokenize(f):
        pos=pos+1
        if not stopwords_removal_words(word):
            tokens.append(clean(word))
            word=clean(word)
            if word in positional:
                if i in positional[word]:
                    positional[word][i].add(pos)
                else:
                    positional[word][i]={pos}
            else:
                positional[word] = {i: {pos}}
print("Positional Index: ")
print()
for x in sorted(positional.items(), key=lambda x: (x[0],x[1])):
    if(x[1]):
      print(x[0])
      for y in sorted(x[1].items(), key=lambda y: (y[0],y[1])):
        print(y[0],": ",sorted(y[1]))
    else:
      print(x[0], ": ", sorted(x[1]))



'''Term Frequency'''


def tf(t,doc):
    count=0
    for x in doc:
        if t == x:
            count=count+1
    return count


'''Inverse Document Frequency'''


def idf(w):
    len_Docs=30
    for x in positional:
        if x == w:
            d=len(positional[x])
            return  math.log(len_Docs/d,10)
    return 0


'''TF-IDF'''


def tf_idf(doc):
    tfIdf=[]
    for w in doc:
        Tf=tf(w,doc)
        Idf=idf(w)
        tfIdf_temp=Tf*Idf
        tfIdf.append(tfIdf_temp)
    return tfIdf


'''Document Vectors'''

vec = []

def document_vector():
    for index,doc in enumerate(docs_tokenize):
        vector =tf_idf(doc)
        vec.append(vector)
document_vector()

def square_vector(vector):
    return [pow(x,2) for x in vector]

def sqrt(arr):
    return arr ** 0.5

def sum(arr):
    result = 0
    for i in arr:
        result += i
    return result


def dot_product(a, b):
    if len(a) != len(b):
        raise ValueError('Vectors must have the same length')
    result = 0
    for i in range(len(a)):
        result += a[i] * b[i]
    return result

'''Cosine Similarity'''

def cos_similarity(q, d,doc):
    query_vec = sqrt(sum(square_vector(q)))
    doc_vec = sqrt(sum(square_vector(doc)))                   #Whole document terms will be taken
    dot = dot_product(q, d)                                   #Only terms appearing in query will be taken from document as eventually all other terms will get zero
    sim=(0.01+ dot / (0.01+(query_vec*doc_vec)))              #0.01 is added for smoothing
    return sim

queries=['Dharamsala to Indore','retirement','test captain','pcb psl','hate','bowling coach','relative comfort', 'possible','batter bowler']


def main():
    label.delete("1.0","end")
    query = query_field.get()
    if query == "":
        label.insert(tk.END, "Kindly Enter The Query For Search")
    else:
        query = stopwords_removal(query)
        query_terms = []

        query_score = []
        for x in query:
            term = clean(x)
            query_terms.append(term)
        q = tf_idf(query_terms)
        sim = []
        for doc_idx, doc in enumerate(docs_tokenize):
            doc_score = 0
            d = list()
            d_temp=list()
            for term in query_terms:
                if term in doc:
                    doc_score += vec[doc_idx][doc.index(term)]
                    d.append(vec[doc_idx][doc.index(term)])
                else:
                    d.append(0)
            query_score.append(doc_score)
            cos_sim=cos_similarity(q,d,vec[doc_idx])
            sim.append(cos_sim)
        results = list(zip(range(1, 31), sim))
        results.sort(key=lambda x: x[1], reverse=True)
        print("Rank\tDoc\tScore")
        label1["text"] = "Rank\tDoc\tScore"
        if results:

            str1 = ''
            for idx, (doc_idx, score) in enumerate(results):
                if score >= 0.05:
                    print(f"{idx + 1}\t{doc_idx}\t{score:.4f}")
                    str1 = str1 + str(idx + 1)+'\t        '+str(doc_idx)+'\t             '+str('%.4f' % (score)) + '\n '
            label.insert(tk.END, str1)
        else:
            label.insert(tk.END, " No Documents Retrieved For this Query")






from tkinter import *
import tkinter as tk
from PIL import ImageTk

if __name__ == "__main__":

    root = Tk()
    bgimg = ImageTk.PhotoImage(file="Your_img.jpg")
    # Specify the file name present in the same directory or else
    # specify the proper path for retrieving the image to set it as background image.
    limg = Label(root, i=bgimg)
    limg.place(x=0, y=0, relwidth=1, relheight=1)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.title("Boolean Retrival Model ")
    root.geometry("500x300")
    query = Label(root, text="Enter Query: ", bg="white", font=("Helvetica", 14))
    query.grid(row=4, column=0)
    query.place(anchor='center', relx=.15, rely=.1)
    query_field = Entry(root)
    query_field.bind("<Return>", query_field.focus_set())
    query_field.grid(row=4, column=1, ipadx="150")
    query_field.place(anchor='center', relx=.65, rely=.1, width=300)
    query = query_field.get()
    submit = Button(root, text="Search", fg="Black", bg="light green", command=main, font=("Helvetica", 14))
    submit.grid(row=30, column=1)
    submit.place(anchor='center', relx=.5, rely=.3)
    label1 = Label(root, text='', bg="white", fg="black", font=("Helvetica", 14))
    label1.grid(row=39, column=1)
    label1.place(anchor='center', relx=.5, rely=.5)
    label = Text(root, bg="white", fg="black", font=("Helvetica", 11),width=30,height=5)
    label.grid(row=40, column=1)
    label.place(anchor='center', relx=.5, rely=.7)

    scrollbar = tk.Scrollbar(root)

    label.bind('<Configure>', lambda e: root.config(height=2))

    scrollbar.config(command=label.yview)
    label.config(yscrollcommand=scrollbar.set)
    scrollbar.place(in_=label, relx=1.0, relheight=1.0, bordermode="outside")

    root.mainloop()






