from flask import Flask, request, render_template
import logging
from logging.handlers import RotatingFileHandler
from flask import jsonify
from time import gmtime, strftime

from session.chatbot import chatbot
from session.nlp.preprocesing import PreProcessor

app = Flask(__name__)
app.config.from_object('config')

#Basic logging
def intializeLog():
    #initialize the log handler
    logHandler = RotatingFileHandler('log/report.log', maxBytes=1000, backupCount=1)

    #set the log handler level
    logHandler.setLevel(logging.INFO)

    #set teh app logger level
    app.logger.setLevel(logging.INFO)

    app.logger.addHandler(logHandler)


# Flask routing apps
@app.route("/")
def indexPage():
    app.logger.info("Chatbot has been deploed" + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    return render_template("index.html")


@app.route("/getMessage")
def getMethod():
    query = request.args.get('message', default='', type=str)
    sentence = PreProcessor().pre_process(query=query)

    response = jsonify(
        Chatbot = chatbot.chatBot.name,
        message = str(chatbot.chatBot.get_response(sentence)),
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    )

    return response

@app.errorhandler(404)
def pageNotFound(e):
    return render_template("HTTP404.html")


if __name__ == '__main__':
    intializeLog()
    app.run(
        port=8080,
        threaded=True
    )
