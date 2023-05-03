# Vector_Space_Model
In this project, I developed a search engine that utilizes the Vector Space Model (VSM) for information retrieval. The VSM is a mathematical model that represents text documents as vectors in a high-dimensional space, where the dimensions correspond to the different terms in the document. The similarity between two documents is then calculated based on the cosine similarity between their corresponding vectors.

To implement the VSM, I first preprocessed the text data by removing stop words and stemming the remaining words to their root forms. I then constructed a document-term matrix, where each row represented a document and each column represented a term. The values in the matrix were the frequency of each term in each document.

Next, I transformed the document-term matrix into a term-frequency inverse-document-frequency (TF-IDF) matrix, which assigns a weight to each term based on its frequency in the document and its rarity across all documents. This helps to reduce the importance of common terms and increase the importance of rare terms.

Finally, I used the TF-IDF matrix to calculate the cosine similarity between the query and each document in the corpus, and ranked the documents based on their similarity scores.

The search engine was evaluated using a test dataset and achieved high precision and recall scores, demonstrating the effectiveness of the VSM for information retrieval.

This project demonstrates my proficiency in natural language processing, information retrieval, and machine learning techniques.
