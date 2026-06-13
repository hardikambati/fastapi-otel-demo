import logging
from fastapi import FastAPI
import otel  # init logging


from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlite3 import SQLite3Instrumentor


from db import init_db, get_conn
from pydantic import BaseModel



app = FastAPI()
logger = logging.getLogger(__name__)


@app.on_event("startup")
def startup():
    print("Initializing database...")
    init_db()
    print("Database initialized.")


# Resource
resource = Resource.create({
    "service.name": "fastapi-loki-demo"
})


# Tracer provider
trace.set_tracer_provider(TracerProvider(resource=resource))
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(
        OTLPSpanExporter(endpoint="http://otel-collector:4318/v1/traces")
    )
)

# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

# Instrument SQLite3
SQLite3Instrumentor().instrument()


@app.get("/hello")
def hello():
    logger.info("hello api called", extra={"user": "hardik"})
    return {"msg": "hello"} 



class StockIn(BaseModel):
    name: str
    price: float

@app.post("/stocks")
def create_stock(stock: StockIn):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO stocks (name, price) VALUES (?, ?)",
        (stock.name, stock.price)
    )
    conn.commit()
    logger.info(f"inserted {stock.name} to DB")
    stock_id = cur.lastrowid
    conn.close()
    return {"id": stock_id, **stock.dict()}


@app.get("/stocks")
def get_stocks():
    conn = get_conn()
    rows = conn.execute("SELECT id, name, price FROM stocks").fetchall()
    conn.close()
    return [
        {"id": r[0], "name": r[1], "price": r[2]}
        for r in rows
    ]
