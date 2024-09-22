# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import init_db
from routes import user, teacher, student, post_like, post, message

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH","PUT", "DELETE"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(teacher.router, prefix="/teachers", tags=["Teachers"])
app.include_router(student.router, prefix="/students", tags=["Students"])
app.include_router(post_like.router, prefix="/post_like", tags=["Post like"])
app.include_router(post.router, prefix="/post", tags=["Post"])
app.include_router(message.router, prefix="/message", tags=["Message"])

@app.on_event("startup")
async def on_startup():
    await init_db()
