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
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text}, timeout=10)
    except:
        pass

PROJECTS = [
    {
        "id": "amurskauto",
        "name": "Авторазбор AmurskAuto",
        "description": "Каталог запчастей, админ-панель, уведомления в Telegram/почту.",
        "url": "https://amurskauto.ru",
        "image": "/static/images/amurskauto.png",
        "details": "Полный цикл разработки: FastAPI, PostgreSQL, Docker. Интеграция с Resend и Telegram. Домен и SSL настроены.",
        "review_text": "«Продавец который правельно подходит к своему делу👍 даже если ты вообще ни чего не понимаешь и не знаешь, то тебе всё объяснял и раскажут👍 к каждому покупателю индивидуальный подход и большое терпение к покупателю, всё понятно и доступно!!! Советую всем👍Отзыв от  Amurskзапчасти, компания авторазбора машин, сделал для нас сайт простой, понятный и доступный👍👍👍 спасибо вам»",
        "payment_imgs": ["/static/images/oplata1_1.jpg", "/static/images/oplata1_2.png"],  # два скриншота
    },
    {
        "id": "evakuator",
        "name": "Эвакуатор 24/7 Балашиха",
        "description": "Яркий лендинг с каруселью, анимациями и кнопкой звонка.",
        "url": "https://evakuator-blh.ru",
        "image": "/static/images/evakuator.png",
        "details": "Адаптивный дизайн, Swiper-слайдер, анимированная кнопка. Настроен мониторинг UptimeRobot.",
        "review_text": "«Данный специалист до конца делает свою работу...»",
        "payment_imgs": ["/static/images/oplata2_1.png"]#, "/static/images/oplata2_2.jpg"], два скриншота (можно позже добавить)
    },
    {
        "id": "volfit",
        "name": "VolFit — Фитнес-платформа",
        "description": "Лендинг с калькулятором калорий, тарифами, формой связи и Telegram-уведомлениями.",
        "url": "https://volfit.onrender.com",
        "image": "/static/images/volfit1.png",
        "details": "Современный дизайн в темных тонах с красными акцентами. Адаптация под мобильные устройства.",
        "review_text": "«Была задача сделать одностраничник сайт для фитнеса зала, сказал все как надо и Владимир сделал за час первую версию и поправил по дизайну ещё на пол часа, сделал быстро и стильно, все работает быстро.»",
        "payment_imgs": [],  # пока нет скриншотов
    },
    {
        "id": "businessflat",
        "name": "BusinessFlat — Аренда квартир",
        "description": "Платформа для аренды квартир с каталогом, фильтрами и формой обратной связи.",
        "url": "https://businessflat.onrender.com",
        "image": "/static/images/BuisnesFlat.png",
        "details": "Разработан на FastAPI, адаптивный дизайн. Интеграция с Telegram для уведомлений.",
        "review_text": "«Понравился подход к работе. Сделал все быстро, сайт удобный.»",
        "payment_imgs": [],  # пока нет скриншотов
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
    success = request.query_params.get("success")
    return HTMLResponse(template.render(projects=PROJECTS, skills=SKILLS, platforms=PLATFORMS, success=success))

@app.post("/contact")
async def contact(name: str = Form(...), contact: str = Form(...), message: str = Form("")):
    text = f"📩 Новое сообщение с портфолио!\nИмя: {name}\nКонтакты: {contact}\nСообщение: {message}"
    send_telegram(text)
    return RedirectResponse("/?success=1", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)