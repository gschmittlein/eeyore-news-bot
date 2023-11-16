from eeyore_backend import news_response

from typing import Union
from fastapi import FastAPI, Depends, Response
from fastapi.security.api_key import APIKey
from fastapi.middleware.cors import CORSMiddleware
import auth
from datamodel import SearchQuery, DefaultResponseSuccess, DefaultResponseFailure

app = FastAPI()

# CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def info(api_key: APIKey = Depends(auth.get_api_key)):
    return "User Authorized"

@app.post("/api/response", status_code = 200)
async def execute_api_search(search_query: SearchQuery,
                             response: Response,
                             api_key: APIKey = Depends(auth.get_api_key)) -> Union[DefaultResponseSuccess, DefaultResponseFailure]:
    
    try:
        search_query_as_dict = dict(
            user_query = search_query.user_query,
            user_person = search_query.user_person
        )
        out = await news_response(search_query_as_dict)

    except Exception as err:
        response.status_code = 555
        return DefaultResponseFailure(error_msg = f"news_response error: {str(err)}")
    
    else:
        if out.get('state') == 'DONE':
            return DefaultResponseSuccess(result = out.get('result'))
        else:
            response.status_code = out.get('response_code', 550)
            return DefaultResponseFailure(error_msg = str(out.get('error_msg')))