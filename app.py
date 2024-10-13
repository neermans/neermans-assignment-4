from flask import Flask, render_template, request, jsonify
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

app = Flask(__name__)

# Preload data and setup LSA components
def load_data():
    print("Loading dataset and preparing LSA components...")
    newsgroups = fetch_20newsgroups(subset='all', remove=('headers', 'footers', 'quotes'))
    vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))
    X = vectorizer.fit_transform(newsgroups.data)
    svd = TruncatedSVD(n_components=100, random_state=42)
    X_reduced = svd.fit_transform(X)
    print("Data loaded and LSA components prepared.")
    return newsgroups, vectorizer, svd, X_reduced

newsgroups, vectorizer, svd, X_reduced_dimensions = load_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()  # Use get_json to correctly parse JSON input
    if not data or 'query' not in data:
        return jsonify({'error': 'No query provided'}), 400

    query = data['query']
    documents, similarities, indices = search_engine(query)
    return jsonify({
        'documents': documents,
        'similarities': similarities.tolist(),
        'indices': indices.tolist()
    })

def search_engine(query):
    """Function to search for top 5 similar documents given a query."""
    query_vector = vectorizer.transform([query])
    query_vector_reduced = svd.transform(query_vector)
    similarities = cosine_similarity(query_vector_reduced, X_reduced_dimensions)[0]
    indices = np.argsort(similarities)[-5:][::-1]

    documents = [{'text': newsgroups.data[idx], 'similarity': similarities[idx]} for idx in indices]
    return documents, similarities[indices], indices

if __name__ == '__main__':
    app.run(debug=True)
