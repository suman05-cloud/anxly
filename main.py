from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# ✅ Load environment variables BEFORE importing routes/services
load_dotenv()

from routes.chat import router
 
app = FastAPI()
 
# ✅ CORS — allows your frontend to talk to this backend
# When deployed on Railway, replace "*" with your actual frontend URL
# e.g. "https://your-frontend.vercel.app"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # 🔧 Change this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
app.include_router(router, prefix="/api")
 
@app.get("/")
def root():
    return {"status": "Backend is running ✅"}