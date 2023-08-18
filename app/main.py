from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient
import datetime
app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

# MongoDB Connection
client = AsyncIOMotorClient("mongodb+srv://saadsgk:saad1234@socialmedia.ia5rj.mongodb.net/")
db = client["blogs"]
sessions_collection = db["blog_app"]

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

from fastapi import HTTPException

from fastapi import Request

@app.post("/book-session/")
async def book_session(
    request: Request, email: str = Form(...), date_time: str = Form(...)
):
    try:
        session_data = {
            "email": email,
            "date_time": date_time,
        }
        await sessions_collection.insert_one(session_data)
        return templates.TemplateResponse(
            "thankyou.html",
            {"request": request},
        )
    except Exception as e:
        alert_message = f"An error occurred: {str(e)}"
        return templates.TemplateResponse(
            "thankyou.html",
            {"request": request, "alert_message": alert_message},
        )

from fastapi import Request

@app.get("/sessions/", response_class=HTMLResponse)
async def get_sessions(request: Request):
    try:
        cursor = sessions_collection.find({}, {"_id": 0, "email": 1, "date_time": 1})
        sessions = await cursor.to_list(length=100)
        return templates.TemplateResponse("sessions.html", {"sessions": sessions, "request": request})
    except Exception as e:
        return templates.TemplateResponse(
            "sessions.html",
            {"alert_message": f"An error occurred: {str(e)}"},
        )


