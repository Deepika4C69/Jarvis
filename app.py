from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import time

# --- Gemini Setup ---
genai.configure(api_key="AIzaSyClPaY2VdVCKjbx0W6X4-JcEOLcNA3tExU")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# --- Flask App Setup ---
app = Flask(__name__, template_folder="templates")
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json['message']
    start = time.time()

    try:
        response = model.generate_content(
            user_input,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                top_p=1.0,
                top_k=40,
                max_output_tokens=256
            )
        )
        reply = response.text
    except Exception as e:
        reply = f"Gemini API error: {e}"

    print("Gemini took", round(time.time() - start, 2), "seconds")
    return jsonify({'input': user_input, 'reply': reply})

@app.route("/wake", methods=["POST"])
def wake():
    return jsonify({"status": "awake"})

@app.route("/sleep", methods=["POST"])
def sleep():
    return jsonify({"status": "sleep"})

if __name__ == "__main__":
    app.run(debug=True)
