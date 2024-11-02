from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class TextVectorizer:
    """Class for extracting text features and performing Doc2Vec vectorization."""

    def __init__(self, vector_size=100, window=5, min_count=1, workers=4):
        """Initializes the TextVectorizer with a Doc2Vec model."""
        self.vector_size = vector_size
        self.model = Doc2Vec(vector_size=self.vector_size, window=window, min_count=min_count, workers=workers)

    def train_model(self, documents):
        """Trains the Doc2Vec model on a corpus of documents.

        :param documents: list: A list of tokenized documents.
        """
        tagged_data = [TaggedDocument(words=doc.split(), tags=[str(i)]) for i, doc in enumerate(documents)]
        self.model.build_vocab(tagged_data)
        self.model.train(tagged_data, total_examples=self.model.corpus_count, epochs=30)

    def vectorize(self, document):
        """Vectorizes a document using the trained Doc2Vec model.

        :param document: str: The document to be vectorized.
        :returns: numpy.ndarray: The vector representation of the document.
        """
        return self.model.infer_vector(document.split())

    def compute_similarity(self, vector1, vector2):
        """Computes cosine similarity between two vectors.

        :param vector1: numpy.ndarray: First document vector.
        :param vector2: numpy.ndarray: Second document vector.
        :returns: float: Cosine similarity between the two vectors.
        """
        print(cosine_similarity([vector1], [vector2]))
        return cosine_similarity([vector1], [vector2])[0][0]

if __name__ == "__main__":
    # Sample usage
    documents = ["This is a sample resume", "This is a sample job description"]
    vectorizer = TextVectorizer()

    # Train the Doc2Vec model on the documents
    vectorizer.train_model(documents)

    # Vectorize a sample resume and job description
    resume_vector = vectorizer.vectorize("This is a sample resume")
    jd_vector = vectorizer.vectorize("This is a sample job description")

    # Compute similarity between the resume and job description
    similarity = vectorizer.compute_similarity(resume_vector, jd_vector)
    print(f"Similarity: {similarity:.4f}")
