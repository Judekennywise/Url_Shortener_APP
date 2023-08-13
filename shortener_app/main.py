import validators
from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from starlette.datastructures import URL
from shortener_app import models, schemas
from shortener_app.database import SessionLocal, engine
from fastapi.responses import RedirectResponse
from shortener_app import crud, models, schemas
from shortener_app.config import get_settings
from shortener_app import schemas
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:4200",
]
app.add_middleware(
    CORSMiddleware,
     allow_origins="*",
      allow_credentials=True,
       allow_methods=["*"],
        allow_headers=["*"]
)


def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/{url_key}")
def forward_to_target_url(
        url_key: str,
        request: Request,
        db: Session = Depends(get_db)
    ):
    db_url = crud.get_db_url_by_key(db=db, url_key=url_key)
    if db_url:
        crud.update_db_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)

@app.get(
    "/admin/{secret_key}",
    name="administration info",
    response_model=schemas.URLInfo,
)
def get_url_info(
    secret_key: str, request: Request, db: Session = Depends(get_db)
):
    db_url= crud.get_db_url_by_secret_key(db, secret_key=secret_key)
    if db_url :
        return get_admin_info(db_url)
    else:
        raise_not_found(request)

@app.get("/")
def read_root():
    return {"message":"Welcome to the URL shortener API :)"} 

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

def get_admin_info(db_url= models.URL) -> schemas.URLInfo:
    base_url = URL(get_settings().base_url)
    admin_endpoint = app.url_path_for(
        "administration info", secret_key=db_url.secret_key
    )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url


@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid. Make sure to include 'http://' or 'https://' in the url")

    db_url = crud.create_db_url(db=db, url=url)
    return get_admin_info(db_url)

@app.delete("/admin/{secret_key}")
def delete_url(
    secret_key: str, request: Request, db: Session = Depends(get_db)
):
    db_url= crud.deactivate_db_url_by_secret_key(db, secret_key=secret_key)
    if db_url :
        message = f"Successfully deleted shortened URL for '{db_url.target_url}'"
        return {"detail": message}
    else:
        raise_not_found(request)