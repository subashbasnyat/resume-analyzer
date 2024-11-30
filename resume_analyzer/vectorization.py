from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.utils import simple_preprocess


class TextVectorizer:
    """Converts text to vector representations."""

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """Initialize the vectorizer with a pre-trained SBERT model."""
        self.model = SentenceTransformer(model_name)

    def calculate_tfidf(self, text):
        """
        Computes TF-IDF vectors
        Args: text (str)
        Returns: numpy.array: TF-IDF vector
        """
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([text])
        return tfidf_matrix.toarray()

    def get_word_embeddings(self, text):
        """
        Generates word embeddings using pre-trained models
        Args: text (str)
        Returns: numpy.array: Word embeddings
        """
        embeddings = self.model.encode(text)
        return embeddings

    def get_document_embedding(self, text, method="sbert"):
        """
        Creates document-level embeddings using either SBERT or Doc2Vec
        Args:
            text (str): Input text to embed
            method (str): Embedding method - either 'sbert' or 'doc2vec'
        Returns:
            numpy.array: Document embedding
        """
        if method.lower() == "sbert":
            return self.get_word_embeddings(text)

        elif method.lower() == "doc2vec":
            # Preprocess text into tokens
            tokens = simple_preprocess(text)

            # Create tagged document
            tagged_doc = TaggedDocument(tokens, [0])  # 0 is a dummy tag

            # Initialize and train Doc2Vec model
            # Using small dimensions for efficiency, can be increased
            model = Doc2Vec(vector_size=100, min_count=1, epochs=30)
            model.build_vocab([tagged_doc])
            model.train(
                [tagged_doc], total_examples=model.corpus_count, epochs=model.epochs
            )

            # Infer vector for the document
            return model.infer_vector(tokens)

        else:
            raise ValueError("Method must be either 'sbert' or 'doc2vec'")

    def calculate_similarity(self, vec1, vec2):
        """
        Computes similarity between vectors using cosine similarity
        Args: vec1, vec2 (numpy.array)
        Returns: float: Similarity score
        """
        # Reshape vectors to 2D arrays as required by sklearn
        vec1_reshaped = vec1.reshape(1, -1)
        vec2_reshaped = vec2.reshape(1, -1)

        # Calculate similarity
        similarity = cosine_similarity(vec1_reshaped, vec2_reshaped)
        return float(similarity[0][0])

    def weighted_section_similarity(self, resume_vec, jd_vec, weights):
        """
        Calculates weighted similarity scores for different sections
        Args:
            resume_vec (dict): Resume section vectors
            jd_vec (dict): Job description section vectors
            weights (dict): Section weights
        Returns: float: Weighted similarity score
        """
        weighted_sum = sum(
            self.calculate_similarity(resume_vec[section], jd_vec[section])
            * weights[section]
            for section in resume_vec
        )
        return weighted_sum


if __name__ == "__main__":
    vectorizer = TextVectorizer()
    resume_vec = vectorizer.get_document_embedding("Resume text", method="sbert")
    jd_vec = vectorizer.get_document_embedding("Job description", method="sbert")
    print(vectorizer.calculate_similarity(resume_vec, jd_vec))
