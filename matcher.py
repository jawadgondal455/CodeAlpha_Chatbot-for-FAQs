
    # matcher.py
    # Loads FAQ data and finds the best matching answer for a user query
    #using TF-IDF vectorization and cosine similarity.


import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from preprocess import clean_text


class FAQMatcher:
    def __init__(self, faq_path: str, threshold: float = 0.35):
        self.threshold = threshold
        self.faqs = self._load_faqs(faq_path)
        self.questions = [item["question"] for item in self.faqs]
        self.cleaned_questions = [clean_text(q) for q in self.questions]

        self.vectorizer = TfidfVectorizer()
        self.question_vectors = self.vectorizer.fit_transform(self.cleaned_questions)

    @staticmethod
    def _load_faqs(path: str):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_best_answer(self, user_query: str) -> str:
        """Return the best matching FAQ answer, or a fallback message."""
        cleaned_query = clean_text(user_query)
        if not cleaned_query:
            return "Could you please rephrase your question?"

        query_vector = self.vectorizer.transform([cleaned_query])
        similarities = cosine_similarity(query_vector, self.question_vectors)[0]

        best_idx = similarities.argmax()
        best_score = similarities[best_idx]

        if best_score < self.threshold:
            return "Sorry, I couldn't find a relevant answer. Please try rephrasing your question."

        return self.faqs[best_idx]["answer"]

    def get_top_matches(self, user_query: str, top_n: int = 3):
        """Return top_n (question, answer, score) matches — useful for debugging."""
        cleaned_query = clean_text(user_query)
        query_vector = self.vectorizer.transform([cleaned_query])
        similarities = cosine_similarity(query_vector, self.question_vectors)[0]

        ranked = sorted(
            range(len(similarities)), key=lambda i: similarities[i], reverse=True
        )[:top_n]

        return [
            (self.faqs[i]["question"], self.faqs[i]["answer"], similarities[i])
            for i in ranked
        ]