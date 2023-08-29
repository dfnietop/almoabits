import uvicorn
from fastapi import FastAPI, Depends, HTTPException

from app.almoabits.almoabits_facade.almoabits_facade import almoabitsFacade
from app.almoabits.almoabits_utils.database import SessionLocal

app = FastAPI()


def db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post("/almoabits/process")
def process_dw(db=Depends(db)):
    try:
        print('entra')
        process = almoabitsFacade(db)
        process.run()
    except HTTPException as e:
        raise e

#
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
