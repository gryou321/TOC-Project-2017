import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import Machine

API_TOKEN = '399226988:AAGIPhHBZQs7izV25clVIUzmlHiHWod1iOA'
WEBHOOK_URL = 'https://cfb28967.ngrok.io'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = Machine(
    states=[
        'init',
        'Hello',
        'Goodbye',
        'Weather1',
        'Weather2',
        'Weather3'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'init',
            'dest': 'Hello',
            'conditions': 'Hello_condition'
        },
        {
            'trigger': 'advance',
            'source': 'init',
            'dest': 'Goodbye',
            'conditions': 'Bye_condition'
        },
        {
            'trigger': 'advance',
            'source': 'init',
            'dest': 'Weather1',
            'conditions': 'Weather_condition'
        },
        {
            'trigger': 'advance',
            'source': 'Weather1',
            'dest': 'Weather2',
            'conditions': 'Where_condition'
        },
        {
            'trigger': 'advance',
            'source': 'Weather2',
            'dest': 'Weather3',
            'conditions': 'When_condition'
        },
        {
            'trigger': 'go_back',
            'source': [
                'Hello',
                'Goodbye',
                'Weather3'
            ],
            'dest': 'init'
        }
    ],
    initial='init',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run()
