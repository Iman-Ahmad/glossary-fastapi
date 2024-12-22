from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/terms/", response_model=list[schemas.Term])
def read_terms(db: Session = Depends(get_db)):
    return crud.get_terms(db)

@app.get("/terms/{keyword}", response_model=schemas.Term)
def read_term(keyword: str, db: Session = Depends(get_db)):
    term = crud.get_term_by_keyword(db, keyword)
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
    return term

@app.post("/terms/", response_model=schemas.Term)
def create_term(term: schemas.TermCreate, db: Session = Depends(get_db)):
    return crud.create_term(db, term)

@app.put("/terms/{keyword}", response_model=schemas.Term)
def update_term(keyword: str, term: schemas.TermUpdate, db: Session = Depends(get_db)):
    updated_term = crud.update_term(db, term, keyword)
    if not updated_term:
        raise HTTPException(status_code=404, detail="Term not found")
    return updated_term

@app.delete("/terms/{keyword}")
def delete_term(keyword: str, db: Session = Depends(get_db)):
    deleted_term = crud.delete_term(db, keyword)
    if not deleted_term:
        raise HTTPException(status_code=404, detail="Term not found")
    return {"detail": "Term deleted"}
