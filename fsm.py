from transitions.extensions import GraphMachine

import requests
from bs4 import BeautifulSoup

import random


class Machine(GraphMachine):
    url = ''
    chose = 1

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

        global url, chose
        url = ''
        chose = 1

    def Hello_condition(self, update):
        text = update.message.text
        return text.lower() == 'Hello' or text.lower() == 'Hi'

    def Bye_condition(self, update):
        text = update.message.text
        return text.lower() == 'Goodbye' or text.lower() == 'Bye'

    def Weather_condition(self, update):
        text = update.message.text
        return text.lower() == '天氣'

    def Where_condition(self, update):
        # Get the lists of cities
        res = requests.get('http://www.cwb.gov.tw/V7/forecast/taiwan/Taipei_City.htm')
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, "html.parser")
        a = soup.select('.CenterMenu > select option')

        for x in a:
            if x.text == update.message.text:
                global url
                url = x['value']
                return True

        update.message.reply_text("台灣沒有這個縣市喔")
        return False

    def When_condition(self, update):
        global chose
        ans = ['1', '2', '3']
        if update.message.text in ans:
            chose = int(update.message.text)
            return True

        update.message.reply_text("輸入時段錯誤!!??")
        return False

    def on_enter_Weather1(self, update):
        update.message.reply_text("你想問哪個縣市的天氣呢?")

    def on_enter_Weather2(self, update):
        update.message.reply_text("你想問哪個時段的天氣呢(1:早 / 2:中 / 3:晚)")

    def on_enter_Weather3(self, update):
        global url, chose
        chose = chose - 1
        res = requests.get(url)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, "html.parser")
        a = soup.select(".FcstBoxTable01 td")
        weather = '溫度 : {}\n濕度 : {}\n天氣狀況 : {}'.format(a[4*chose], a[4*chose+3], a[4*chose+1])
        update.message.reply_text(weather)

    def on_enter_Hello(self, update):
        update.message.reply_text(random.choice(['你好', '哈囉', 'Hi', 'Hello']))
        self.go_back(update)
    def on_enter_Goodbye(self, update):
        update.message.reply_text(random.choice(['掰掰', '再見', 'Goodbye', 'Bye~']))
        self.go_back(update)

    def on_enter_Weather3(self, update):
        self.go_back(update)
