
import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
import datetime
import json
import logging
import sys
import time
import azure.functions as func
import requests, xmltodict
from bs4 import BeautifulSoup
from azure.data.tables import TableServiceClient
from azure.core.exceptions import HttpResponseError
from encodings import utf_8_sig  # 액셀파일에서 한글깨질때

sys.path.append("./")
from . import bus_data_file

token = '5854936368:AAFizpzCJ8IFuHO-X1TyVGnInRVHQMNbMV8'
id = "5803830393"
bot = telegram.Bot(token)

# updater
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
#봇
updater.start_polling()

def handler(update, context):
    user_text = update.message.text 
    if user_text=="버스": #사용자가 버스 입력시 동작
        key = 1
        bus_info=bus_data_file.crwl_bus(key)
        bot.send_message(chat_id=id,text=bus_info)
        bot.sendMessage(chat_id=id,text=info_message)


#들어간 코드 유지해주는 코드   
echo_handler = MessageHandler(Filters.text, handler)
dispatcher.add_handler(echo_handler)


def main(mytimer: func.TimerRequest, tablePath:func.Out[str]) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info("The timer is past due!")
    key = 0
    tags = bus_data_file.crwl_bus(key)
    bus_data = {
        "첫번째버스": tags[0],
        "첫번째버스도착시간": tags[1],
        "첫번째버스두번째도착시간": tags[2],
        "두번쨰버스": tags[3],
        "두번쨰버스도착시간": tags[4],
        "두번쨰버스두번째도착시간": tags[5],
        "세번째버스": tags[6],
        "세번째버스도착시간": tags[7],
        "세번째버스두번째도착시간": tags[8], 
        "PartitionKey":"bus_time",
        "RowKey": time.time()
    }
    print(bus_data)
    tablePath.set(json.dumps(bus_data))