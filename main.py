# app/main.py
from fastapi import FastAPI
from config import init_db
from routes import user, teacher, student, post_like, post, message

app = FastAPI()

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
