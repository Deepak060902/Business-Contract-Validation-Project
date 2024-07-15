from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


def preprocess_text(text):
    return ' '.join(text.lower().split())

def calculate_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

def compare_clauses(classified_clauses, template_clauses, threshold=0.9):
    deviations = {}

    for clause_name, clause_text in classified_clauses.items():

        if clause_text:
            if clause_name in template_clauses.keys():
                template_text = template_clauses[clause_name]
                similarity = calculate_similarity(
                    preprocess_text(clause_text),
                    preprocess_text(template_text)
                )
                if similarity < threshold:
                    deviations[clause_name] = [clause_text, template_text,similarity]
            else:
                deviations[clause_name] =  [clause_text, template_text, 0.0]
    return deviations
     
def detect_deviations(actual_clauses,template_clauses):

    deviations = compare_clauses(actual_clauses, template_clauses)
 
    return deviations

