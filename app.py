from flask import Flask, request, render_template
from graph import research_app
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/research", methods=["POST"])
def research():
    topic = request.form["topic"]
    
    result = research_app.invoke({
        "topic": topic,
        "research": "",
        "analysis": "",
        "report": ""
    })
    
    return render_template("result.html", report=result["report"])

if __name__ == "__main__":
    app.run(debug=True)