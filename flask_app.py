from flask import Flask, render_template, request, Response, jsonify
from chatbot import ChatBot

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
    
    # flask accepts an entire message history from the website in a POST request, then
    # 'simulates' all the user messages being handled by the chatbot, so the chatbot is
    # 'aware' of all previous messages sent.
    messages = message.split("~^%!*$*!%^~")

    cbot = ChatBot()
    result = None
    for message in messages:
        result = cbot.handle_message(message)
    r = jsonify({"message": message, "response": result})
    return r
