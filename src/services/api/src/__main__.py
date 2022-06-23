from fastapi import FastAPI

from src.impl.database import database

app = FastAPI()
app.state.database = database


@app.on_event("startup") # type: ignore
async def startup() -> None:
    _database = app.state.database

    if not _database.is_connected:
        await _database.connect()


@app.on_event("shutdown") # type: ignore
async def shutdown() -> None:
    _database = app.state.database

    if _database.is_connected:
        await _database.disconnect()
