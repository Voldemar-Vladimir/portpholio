from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from mako.lookup import TemplateLookup
import os
import requests

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = TemplateLookup(directories=["templates"])

TELEGRAM_TOKEN = "8601793998:AAH0Kqg5_eR9rccweqscC3EVAIiwHovmq7A"
TELEGRAM_CHAT_ID = "5977647337"

def send_telegram(text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        response = requests.post(
            url,
            json={"chat_id": TELEGRAM_CHAT_ID, "text": text},
            timeout=15
        )
        print(f"Telegram API response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")

PROJECTS = [
    {
        "id": "amurskauto",
        "name": "Авторазбор AmurskAuto",
        "description": "Каталог запчастей, админ-панель, уведомления в Telegram/почту.",
        "url": "https://amurskauto.ru",
        "image": "/static/images/amurskauto.png",
        "details": "Полный цикл разработки: FastAPI, PostgreSQL, Docker. Интеграция с Resend и Telegram. Домен и SSL настроены.",
        "review_text": "«Продавец который правельно подходит к своему делу👍 даже если ты вообще ни чего не понимаешь и не знаешь, то тебе всё объяснял и раскажут👍 к каждому покупателю индивидуальный подход и большое терпение к покупателю, всё понятно и доступно!!! Советую всем👍Отзыв от  Amurskзапчасти, компания авторазбора машин, сделал для нас сайт простой, понятный и доступный👍👍👍 спасибо вам»",
        "payment_img": "/static/images/oplata1.jpg",
    },
    {
        "id": "evakuator",
        "name": "Эвакуатор 24/7 Балашиха",
        "description": "Яркий лендинг с каруселью, анимациями и кнопкой звонка.",
        "url": "https://evakuator-blh.onrender.com",
        "image": "/static/images/evakuator.png",
        "details": "Адаптивный дизайн, Swiper-слайдер, анимированная кнопка. Настроен мониторинг UptimeRobot.",
        "review_text": "«Данный специалист до конца делает свою работу...»",
        "payment_img": "/static/images/oplata2.jpg",  # исправил на .jpg, если у тебя файл jpg
    },
]

SKILLS = [
    "Python", "FastAPI", "SQLAlchemy", "PostgreSQL", "Redis",
    "Docker", "Docker Compose", "Git", "GitLab CI/CD", "Linux",
    "Nginx", "REST API", "GraphQL", "Sentry", "Prometheus",
    "Telegram Bot API", "Resend", "Jinja2/Mako", "HTML/CSS", "JavaScript"
]

PLATFORMS = [
    {"name": "Telegram", "url": "https://t.me/Voldemar_Vladimir_IT"},
    {"name": "Kwork", "url": "https://kwork.ru/user/MasterVladimir"},
    {"name": "Авито", "url": "ссылка-на-авито"},
    {"name": "Юла", "url": "ссылка-на-юлу"},
]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    template = templates.get_template("index.html")
    return HTMLResponse(template.render(projects=PROJECTS, skills=SKILLS, platforms=PLATFORMS))

@app.post("/contact")
async def contact(name: str = Form(...), contact: str = Form(...), message: str = Form("")):
    text = f"📩 Новое сообщение с портфолио!\nИмя: {name}\nКонтакты: {contact}\nСообщение: {message}"
    send_telegram(text)
    return RedirectResponse("/?success=1", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)