import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist

nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text.lower()

def extract_key_info(text):
    parties = re.findall(r'(?:between|party)[:\s]+([^,\.]+)', text, re.IGNORECASE)
    # dates = re.findall(r'\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December),?\s+\d{4}', text)
    
    return {
        'parties': parties,
    }

def summarize_text(text, num_sentences=5):
    sentences = sent_tokenize(text)
    words = word_tokenize(preprocess_text(text))
    
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    
    freq = FreqDist(words)
    
    scores = {}
    for i, sentence in enumerate(sentences):
        for word in word_tokenize(preprocess_text(sentence)):
            if word in freq:
                if i in scores:
                    scores[i] += freq[word]
                else:
                    scores[i] = freq[word]
    
    summary_sentences = sorted(scores, key=scores.get, reverse=True)[:num_sentences]
    summary = [sentences[i] for i in sorted(summary_sentences)]
    
    return ' '.join(summary)

def summarize_contract(contract_text):
    key_info = extract_key_info(contract_text)
    summary = summarize_text(contract_text)
    return summary
    # return ' '.join(key_info['parties'])



