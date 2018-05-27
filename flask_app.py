from flask import Flask, render_template, request, Response, jsonify

app = Flask(__name__)

# client-side stored messages. Displayed using javascript.
@app.route('/')
def hello_world():
    # TO-DO: change the name of the chatbot ._. we do not want to see any group submit 'Hello, world!' chatbots.
    return render_template("index.html", chatbot_title = "Hello, world!")

@app.route('/request_response', methods=["POST"])
def generate_response():
    message = str(request.data.decode("utf-8"))
    if len(message) == 0:
        return Response("no u", status=500)

    r = jsonify({"message": message, "response": "Hello, world!"})
    return r
