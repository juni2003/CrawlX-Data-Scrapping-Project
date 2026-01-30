from fastapi import FastAPI, Depends, Query
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from .db import SessionLocal, engine
from .models import Base
from . import crud, schemas
import io
import csv

app = FastAPI(title="Scraper Backend API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"status": "ok", "message": "Scraper API running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/items", response_model=list[schemas.ScrapedItemOut])
def list_items(
    skip: int = 0,
    limit: int = Query(50, le=200),
    db: Session = Depends(get_db),
):
    return crud.get_items(db, skip=skip, limit=limit)


@app.get("/search", response_model=list[schemas.ScrapedItemOut])
def search_items(
    q: str,
    skip: int = 0,
    limit: int = Query(50, le=200),
    db: Session = Depends(get_db),
):
    return crud.search_items(db, q=q, skip=skip, limit=limit)



@app.get("/items/export")
def export_items_json(db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=0, limit=1000)
    data = [schemas.ScrapedItemOut.model_validate(i).model_dump(mode="json") for i in items]
    return JSONResponse(content=data)



@app.get("/items/export/csv")
def export_items_csv(db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=0, limit=1000)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "source", "title", "url", "summary", "tags", "published_at", "scraped_at"])

    for i in items:
        writer.writerow([
            i.id, i.source, i.title, i.url, i.summary, i.tags, i.published_at, i.scraped_at
        ])

    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=scraped_items.csv"}
    )