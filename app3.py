# encoding: utf-8
import requests
import json
from flask import Flask
from datetime import datetime
from flask import jsonify, request


app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return jsonify({
        "message": "this endpoint is active"
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    reply_to_line(request.json)
    return '', 200, {}

def reply_to_line(body):
    for event in body['events']:
        responses = []

        replyToken = event['replyToken']
        type = event['type']
        
        if type == 'message':
            message = event['message']
            
            if message['type'] == 'text':
                # そのままオウム返し
                responses.append(LineReplyMessage.make_text_response(message['text']))
            else:
                # テキスト以外のメッセージにはてへぺろしておく
                responses.append(LineReplyMessage.make_text_response('てへぺろ'))

        # 返信する
        LineReplyMessage.send_reply(replyToken, responses)


class LineReplyMessage:
    ReplyEndpoint = 'https://api.line.me/v2/bot/message/reply'
    AccessToken = '1SmGKlg59CG8VNJQFGSRoHhUbbbtYnyoePC0S3DfEbZkYS0kKfueCEYNQz6L/zPbywLbATf1H6BAWnr+K2Ii5U8Bf5JddLN8LklJ/E74wgS6LP3I4cYTEeNVIPE2vu79qBdsaIwxRfzlkFocAWmIzAdB04t89/1O/w1cDnyilFU='

    @staticmethod
    def make_text_response(text):
        return {
            'type': 'text',
            'text': text
        }

    @staticmethod
    def send_reply(replyToken, messages):
        reply = {
            'replyToken': replyToken,
            'messages': messages
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(LineReplyMessage.AccessToken)
        }

        requests.post(
            LineReplyMessage.ReplyEndpoint,
            data=json.dumps(reply),
            headers=headers)
