from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.services.database_initializer import initialize_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database when the application starts
    initialize_database()
    yield
    # Perform any cleanup tasks when the application shuts down (if needed)