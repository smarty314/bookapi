import psycopg2
from fastapi import FastAPI,Request,Depends
from fastapi import APIRouter
from config import settings
from schemas import APIResponse
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
import httpx



app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
)

# Define the auth scheme and access token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

books_router = APIRouter()

# Call the Okta API to get an access token
def retrieve_token(authorization, issuer, scope='items'):
    headers = {
        'accept': 'application/json',
        'authorization': authorization,
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'scope': scope,
    }
    url = issuer + '/v1/token'

    response = httpx.post(url, headers=headers, data=data)

    if response.status_code == httpx.codes.OK:
        return response.json()
    else:
        raise HTTPException(status_code=400, detail=response.text)


# Get auth token endpoint
@app.post('/token')
def login(request: Request):
    return retrieve_token(
        request.headers['authorization'],
        "https://dev-01515259.okta.com/oauth2/default",
        'myscope'
    )

def validate_remotely(token, issuer, clientId, clientSecret):
    headers = {
        'accept': 'application/json',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
    }
    data = {
        'client_id': clientId,
        'client_secret': clientSecret,
        'token': token,
    }
    url = issuer + '/v1/introspect'

    response = httpx.post(url, headers=headers, data=data)

    return response.status_code == httpx.codes.OK and response.json()['active']


def validate(token: str = Depends(oauth2_scheme)):
    res = validate_remotely(
        token,
        "https://dev-01515259.okta.com/oauth2/default",
    )

    if res:
        return True
    else:
        raise HTTPException(status_code=400)
        
def sql(sql:str):
    try:
        conn = psycopg2.connect(
            host="db", 
            port="5432", 
            options="-c search_path=dbo,public",
            user='oreilly',
            password='hunter2')

        cursor = conn.cursor()
        cursor.execute(sql)
        table = cursor.fetchall()
        conn.close()
        return table
    except Exception as e:
        raise e
        print("I am unable to connect to the database")

@books_router.get('/title', response_model=APIResponse)
def get_books_by_title(search:Optional[str] = None, token: str = Depends(oauth2_scheme)):
    if search is None:
        search = ''
    try:
        books = sql("SELECT title,authors,isbn from works where title ilike '%%%s%%'" % search)
        return APIResponse(
            search = search,
            books = books,
            count = len(books),
            status_code="200")
    except Exception as e:
        print(e)
        return APIResponse(books=[],
            status_code="401")

@books_router.get('/authors', response_model=APIResponse)
def get_books_by_authors(search:Optional[str] = None, token: str = Depends(oauth2_scheme)):
    if search is None:
        search = ''
    try:
        books = sql("SELECT title,authors,isbn from works where author ilike '%%%s%%'" % search)
        return APIResponse(
        search = search,
        books = books,
        count = len(books),
        status_code="200")
    except Exception as e:
        print(e)
        return APIResponse(books=[],
        status_code="401")

@books_router.get('/isbn', response_model=APIResponse)
def get_books_by_isbn(search:Optional[str] = None, token: str = Depends(oauth2_scheme)):
    if search is None:
        search = ''
    try:
        books = sql("SELECT title,authors,isbn from works where isbn ilike '%%%s%%'" % search)
        return APIResponse(
        search = search,
        books = books,
        count = len(books),
        status_code="200")
    except Exception as e:
        print(e)
        return APIResponse(books=[],
        status_code="401")

@books_router.get('/description', response_model=APIResponse)
def get_books_by_description(search:Optional[str] = None, token: str = Depends(oauth2_scheme)):
    if search is None:
        search = ''
    try:
        books = sql("SELECT title,authors,isbn from works where description ilike '%%%s%%'" % search)
        return APIResponse(
            search = search,
            books = books,
            count = len(books),
            status_code="200")
    except Exception as e:
        print(e)
        return APIResponse(books=[],
                status_code="401")
        return APIResponse(books=[],
        status_code="401")

app.include_router(
    books_router,
    prefix="/books",
    tags=["books"]
)