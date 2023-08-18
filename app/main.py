from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from pydantic import BaseModel
app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

# MongoDB Connection
client = AsyncIOMotorClient("mongodb+srv://saadsgk:saad1234@socialmedia.ia5rj.mongodb.net/")
db = client["blogs"]
sessions_collection = db["blog_app"]

class SessionCreate(BaseModel):
    email: str
    date_time: str

class SessionResponse(BaseModel):
    email: str
    date_time: str

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/book-session/", response_class=HTMLResponse)
async def book_session(request: Request):
    try:
        session_data = SessionCreate(**await request.form())

        await sessions_collection.insert_one(session_data.dict())
        return templates.TemplateResponse(
            "thankyou.html",
            {"request": request, "alert_title": "Booking Successful", "alert_message": "Your session has been booked."},
        )
    except Exception as e:
        alert_message = f"An error occurred: {str(e)}"
        return templates.TemplateResponse(
            "thankyou.html",
            {"request": request, "alert_message": alert_message},
        )

@app.post("/delete-session/", response_class=HTMLResponse)
async def delete_session(request: Request):
    try:
        session_data = SessionCreate(**await request.form())

        delete_result = await sessions_collection.delete_one(session_data.dict())
        if delete_result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return templates.TemplateResponse(
            "thankyou.html",
            {"request": request, "alert_title": "Deletion Successful", "alert_message": "Session deleted successfully."},
        )
    except Exception as e:
        return templates.TemplateResponse(
            "thankyou.html",
            {"request": request, "alert_message": f"An error occurred: {str(e)}"},
        )


@app.get("/sessions/", response_class=HTMLResponse)
async def get_sessions(request: Request):
    try:
        cursor = sessions_collection.find({}, {"_id": 0, "email": 1, "date_time": 1})
        sessions = await cursor.to_list(length=100)
        session_responses = [SessionResponse(**session) for session in sessions]
        return templates.TemplateResponse("sessions.html", {"sessions": session_responses, "request": request})
    except Exception as e:
        return templates.TemplateResponse(
            "sessions.html",
            {"alert_message": f"An error occurred: {str(e)}"},
        )
