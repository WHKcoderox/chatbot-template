function gotoBottom(id){
   var element = document.getElementById(id);
   element.scrollTop = element.scrollHeight - element.clientHeight;
}

function fetch_all_messages(new_msg) {
    var user_msgs = document.getElementsByClassName("fromuser");
    msg_history = "";
    for (var i = 0, len = user_msgs.length; i < len; i++) {
        msg_history += user_msgs.value + "~^%!*$*!%^~"; // separator.
    }
    return msg_history + new_msg;
}

// some setup for the request for Flask to return the chatbot's response.
var url = "http://meverynoob.pythonanywhere.com/request_response";
var method = "POST";

// You REALLY want shouldBeAsync = true.
// Otherwise, it'll block ALL execution waiting for server response.
var shouldBeAsync = true;
var request;

function receive_message(e) {
    e.preventDefault(); // By default, the page reloads. This prevents that refresh.
    var postData = fetch_all_messages(document.getElementById('messagebox').value);
    document.getElementById('messagebox').value = "";
    request = new XMLHttpRequest();
    request.onload = load_response;
    request.open(method, url, shouldBeAsync);
    request.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");
    request.send(postData);
}

function load_response() {
    var status = request.status; // HTTP response status, e.g., "200 OK" (Success!)
    var data = JSON.parse(request.responseText); // since it's initially a string, I need to convert it into a JSON format.

    if (status == 200) {
        document.getElementById('default').style.display = 'none';
        var message_space = document.getElementById('messagespace');
        message_space.insertAdjacentHTML('beforeend', "<div class='msgcontainer'><p class='message fromuser'>" + data.message + "</p></div>");
        message_space.insertAdjacentHTML('beforeend', "<div class='msgcontainer'><p class='message fromchatbot'>" + data.response + "</p></div>");
        gotoBottom('messagespace')
    }
}

function init() {
    document.getElementById('fields').onsubmit = receive_message;
}

window.onload = init;
