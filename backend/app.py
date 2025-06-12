from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

API_TOKEN = os.getenv("HF_TOKEN")

def query_hf_api(payload, model):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    return requests.post(
        f"https://api-inference.huggingface.co/models/{model}",
        headers=headers, json=payload
    ).json()

@app.route("/summarize", methods=["POST"])
def summarize():
    text = request.json.get("text")
    output = query_hf_api({"inputs": text}, "facebook/bart-large-cnn")
    summary = output[0].get("summary_text", "No summary.") if isinstance(output, list) else output.get("error", str(output))
    return jsonify({"summary": summary})

@app.route("/question", methods=["POST"])
def question():
    data = request.json
    output = query_hf_api({"inputs": {"question": data.get("question"), "context": data.get("text")}}, "deepset/roberta-base-squad2")
    answer = output.get("answer", "No answer found." if isinstance(output, dict) else "Check logs")
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
