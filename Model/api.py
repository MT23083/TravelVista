from flask import Flask, jsonify, request
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.faiss import FAISS
import sys
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/process_text": {"origins": "http://localhost:3000"}})

# Initialize Langchain components
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
modelPath = "sentence-transformers/all-MiniLM-l6-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
embeddings = HuggingFaceEmbeddings(model_name=modelPath, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)

# Define API route
@app.route('/process_text', methods=['GET'])
def process_text():
    # Extract text from query parameters
    text = request.args.get('text')
    
    # Process text
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    search_results = new_db.similarity_search_with_relevance_scores(text, k=30)

    # Format results with unique identifiers
    final_results = []
    for doc_tuple in search_results[0:10]:
        doc = doc_tuple[0]  # Access the Document object in the tuple
        rating = str(int(doc.metadata['Rating'] * 100)).zfill(2)  # Convert and pad rating to two digits
        unique_id = f"{doc.metadata['Response']}_{rating}"  # Compose unique identifier
        doc_data = {
            'uid': unique_id,
            'page_content': doc.page_content,
            'metadata': doc.metadata
        }
        final_results.append(doc_data)

    # Return response
    return jsonify({'results': final_results})

# Run Flask app
if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9001
    app.run(port=port, host='0.0.0.0', debug=True)
