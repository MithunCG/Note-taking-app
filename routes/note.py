from fastapi import APIRouter
from models.note import Note
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from config.db import conn
from schemas.note import noteEntity, notesEntity

note = APIRouter()
templates = Jinja2Templates(directory="templates")

@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs = conn.notes.notes.find({})
    newDocs = []
    for doc in docs:
        newDocs.append({
            "id": doc.get("_id"),
            "title": doc.get("title", "Untitled"),
            "desc": doc.get("desc", ""),
            "important": doc.get("important", False),
        })

    return templates.TemplateResponse("index.html", {"request": request, "newDocs": newDocs})

@note.post("/")
async def create_item(request: Request):
    form = await request.form()
    formDict = dict(form)

    # Convert "important" field to boolean (True if checkbox was checked)
    is_important = form.get("important") == "on"

    # Create a new note dictionary with proper types
    note_data = {
        "title": formDict.get("title", ""),
        "desc": formDict.get("desc", ""),
        "important": is_important,
    }

    # Insert into MongoDB
    conn.notes.notes.insert_one(note_data)

    return {"Success": True}


    