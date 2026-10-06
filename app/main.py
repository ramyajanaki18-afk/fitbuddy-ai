from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router

app = FastAPI()

# ⚠️ மிகவும் முக்கியமானது: CSS மற்றும் Static files-ஐ மவுண்ட் செய்ய வேண்டும்
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")

# Routes-ஐ இணைக்கிறோம்
app.include_router(router)