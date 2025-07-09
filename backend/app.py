from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)

# Allow CORS for Vercel frontend (or use origins="*" temporarily for testing)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "https://docqa-tool.vercel.app"}})

API_KEY = os.getenv("API_KEY")

def query_hf_api(payload, model):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.post(
        f"https://api-inference.huggingface.co/models/{model}",
        headers=headers, json=payload
    )
    return response.json()

@app.route("/summarize", methods=["POST", "OPTIONS"])
def summarize():
    if request.method == "OPTIONS":
        return jsonify({}), 200

    text = request.json.get("text")
    output = query_hf_api({"inputs": text}, "facebook/bart-large-cnn")

    summary = (
        output[0].get("summary_text", "No summary.")
        if isinstance(output, list)
        else output.get("error", str(output))
    )
    return jsonify({"summary": summary})

@app.route("/question", methods=["POST", "OPTIONS"])
def question():
    if request.method == "OPTIONS":
        return jsonify({}), 200

    data = request.json
    output = query_hf_api(
        {"inputs": {"question": data.get("question"), "context": data.get("text")}},
        "deepset/roberta-base-squad2"
    )
    answer = (
        output.get("answer", "No answer found.")
        if isinstance(output, dict)
        else "Check logs"
    )
    return jsonify({"answer": answer})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
