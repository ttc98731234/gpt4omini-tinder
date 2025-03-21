import datetime
import os
import random
from src.chatgpt import ChatGPT, DALLE
from src.models import OpenAIModel
from src.tinder import TinderAPI
from src.dialog import Dialog
from src.logger import logger
from opencc import OpenCC
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.base import JobLookupError
from dotenv import load_dotenv
from fastapi import FastAPI, BackgroundTasks
import uvicorn
import pytz

load_dotenv('.env')

# 升級為使用 gpt4o mini
models = OpenAIModel(api_key=os.getenv('OPENAI_API'),
                     model_engine="gpt4o-mini")

chatgpt = ChatGPT(models)
dalle = DALLE(models)
dialog = Dialog()
app = FastAPI()

# 使用 UTC 時區
scheduler = AsyncIOScheduler(timezone=pytz.UTC)
cc = OpenCC('s2t')
TINDER_TOKEN = os.getenv('TINDER_TOKEN')

# 自動滑動模組配置
SWIPE_TIME_RANGES = [("09:00", "12:00"), ("18:00", "22:00")]
DAILY_SWIPE_LIMIT = 100
swipe_count = 0

@scheduler.scheduled_job("cron", minute='*/5', second=0, id='reply_messages')
def reply_messages():
    if not TINDER_TOKEN:
        logger.error("TINDER_TOKEN is not set. Please add it to your environment variables.")
        return
        
    try:
        tinder_api = 8397db6c-eacb-4cb0-8931-5ef16f27a1be (TINDER_TOKEN)
        profile = 8397db6c-eacb-4cb0-8931-5ef16f27a1be.profile()
        user_id = profile.id
    except Exception as e:
                last_message = 'me'
            else:
                from_user_id = lastest_message.to_id
                to_user_id = lastest_message.from_id
                last_message = 'other'
            sent_date = lastest_message.sent_date
            if last_message == 'other' or (sent_date + datetime.timedelta(days=1)) < datetime.datetime.now():
                content = dialog.generate_input(from_user_id, to_user_id, chatroom.messages[::-1])
                response = chatgpt.get_response(content)
                if response:
                    response = cc.convert(response)
                    if response.startswith('[Sender]'):
                        chatroom.send(response[8:], from_user_id, to_user_id)
                    else:
                        chatroom.send(response, from_user_id, to_user_id)
                logger.info(f'Content: {content}, Reply: {response}')

@scheduler.scheduled_job("cron", minute='*/10', id='auto_swipe')
def auto_swipe():
    if not TINDER_TOKEN:
        logger.error("TINDER_TOKEN is not set. Please add it to your environment variables.")
        return
        
    global swipe_count
    current_time = datetime.datetime.now().time()
    for start, end in SWIPE_TIME_RANGES:
        if start <= current_time.strftime("%H:%M") <= end and swipe_count < DAILY_SWIPE_LIMIT:
            try:
                tinder_api = TinderAPI(TINDER_TOKEN)
                if random.random() < 0.5:  # 隨機化滑動行為
                    # Note: swipe_right method is called but not implemented in the shown code
                    # tinder_api.swipe_right()
                    swipe_count += 1
                    logger.info(f'Swiped right. Total swipes: {swipe_count}')
            except Exception as e:
                logger.error(f"Error in auto_swipe: {str(e)}")
            break

@app.on_event("startup")
async def startup():
    scheduler.start()

@app.on_event("shutdown")
async def shutdown():
    try:
        scheduler.remove_job('reply_messages')
        scheduler.remove_job('auto_swipe')
    except JobLookupError:
        logger.warning("Job not found during shutdown.")

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8080)