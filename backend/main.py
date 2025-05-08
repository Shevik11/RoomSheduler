from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import days, rooms, lessons, groups, teachers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Підключення роутера
app.include_router(days.router)
app.include_router(rooms.router)
app.include_router(lessons.router)
app.include_router(groups.router)
app.include_router(teachers.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
