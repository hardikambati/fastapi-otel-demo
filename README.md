# Opentelemetry Instrumentation Demo using FastAPI

A simple demo showing how to instrument **logs and traces** in a single **FastAPI** service using **OpenTelemetry**.

## What’s Included
- API request spans  
- Database call spans  
- Application logs  

Traces are stored in **Tempo**, logs in **Loki**, and everything is visualized in **Grafana**.

## Setup
```bash
docker compose up --build -d
```

## Blog
Detailed explanation and implementation steps:  
https://medium.com/@hardikambati69/part-2-stop-flying-blind-instrument-your-fastapi-app-using-opentelemetry-implementation-56d82fc9e93a