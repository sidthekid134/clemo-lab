from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config.settings import settings
from .database.database import create_db_and_tables
from .routers import placeholder, story

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(placeholder.router)
app.include_router(story.router)


@app.on_event("startup")
async def on_startup():
    """Initialize the application on startup."""
    create_db_and_tables()


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to the Placeholder API"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}