#내장 모듈
import os
from urllib.request import urlopen
#외장 모듈
from bs4 import BeautifulSoup
from github import Github
import telegram

#레퍼런스
#github: https://pygithub.readthedocs.io/
#python-telegram-bot: https://python-telegram-bot.readthedocs.io/

'''
#ID 받아오기
chat_token = os.environ["CHAT_BOT_TOKEN"]
bot = telegram.Bot(token = chat_token)
updates = bot.getUpdates()
for u in updates:
    print(u.message['chat']['id'])
''' 

#크롤링
url = "https://store.sony.co.kr/handler/ViewProduct-Start?productId=32851960"
target = "A7S III"

#BeautifulSoup4
html = urlopen(url)
bsObject = BeautifulSoup(html, "html.parser")
parent_path = bsObject.find("p", class_="btnArea")
links = parent_path.find_all("a")
if links[1].text == "일시품절":
    #일시 품절
    title = "재고 없음"
    body = "재고가 없습니다."
    disable_notification = True
else:
    #입고 완료
    title = "입고 완료"
    body = "입고가 완료되었습니다! 지금 바로 구매하세요."
    disable_notification = False

    #텔레그램 메시지 보내기
    #버튼 생성
    keyboard = [
        [telegram.InlineKeyboardButton(text="사이트로 이동", url=url)]
    ]
    text = "<b>{target}: {title}</b>\n{body}\n{url}".format(target=target, title=title, body=body)
    chat_token = os.environ["CHAT_BOT_TOKEN"]
    chat_id = os.environ["CHAT_USER_ID"]
    bot = telegram.Bot(token = chat_token)
    bot.send_message(
        chat_id = chat_id,
        text = text,
        parse_mode="HTML",
        disable_notification=disable_notification,
        reply_markup=telegram.InlineKeyboardMarkup(keyboard)
    )

#이슈 남기기
g = Github(os.environ["MY_GITHUB_TOKEN"])
repo = g.get_user().get_repo("telegram_bot")
repo.create_issue(title="{target}: {title}".format(target=target, title=title), body="{body}\n{url}".format(body=body, url=url))
#이슈 클로징
open_issues = repo.get_issues(state='open')
for issue in open_issues:
    issue.edit(state='closed')
