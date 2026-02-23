from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
from .engine import TradingEngine
from .market_data import YFinanceProvider
from .account import AccountManager
from .strategy import StrategyModule
import threading
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("API")

# Global State
engine: TradingEngine = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global engine
    logger.info("Initializing Trading Engine...")
    market_data = YFinanceProvider()
    account = AccountManager(initial_cny=100000.0, initial_usd=0.0)
    strategy = StrategyModule(short_window=5, long_window=20)
    engine = TradingEngine(market_data, account, strategy, interval=5)
    logger.info("Engine Initialized")

    yield

    # Shutdown
    if engine:
        engine.stop()

app = FastAPI(lifespan=lifespan)

# Enable CORS for Next.js (usually on port 3000)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConfigUpdate(BaseModel):
    short_window: int
    long_window: int

@app.get("/status")
def get_status():
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return engine.get_status()

@app.post("/start")
def start_engine():
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    engine.start()
    return {"message": "Engine started"}

@app.post("/stop")
def stop_engine():
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    engine.stop()
    return {"message": "Engine stopped"}

@app.post("/config")
def update_config(config: ConfigUpdate):
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    try:
        engine.update_strategy_parameters(config.short_window, config.long_window)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Configuration updated"}

@app.get("/history")
def get_history():
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return engine.account.get_history()
