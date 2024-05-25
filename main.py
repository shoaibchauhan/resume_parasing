import os
import django
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from resume_selector.controller import resume

print("Setting DJANGO_SETTINGS_MODULE")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "resume_parasing.settings")

print("Initializing Django")
django.setup()

print("Creating FastAPI instance")
app = FastAPI()

print("Including router")
app.include_router(resume, prefix="/api")

@app.get("/", response_class=HTMLResponse)
def read_root():
    return "<h1>Welcome to the FastAPI & Django Integration</h1>"
