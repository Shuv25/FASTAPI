from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

@app.get("/")
async def root():
    return {"mesaage":"Hello World"}

@app.get("/socila_media_post")  #in get we simply fetch data from the server
async def data():
    content = ["Hello kitty","Hello Mini"]
    return {"post":content}

@app.post("/details/{name}") # in post we pass some data to fetch data from the server 
async def get_details(name:str):
    name = name.title()
    return {"message":f"Hi there! {name}"}


class InputData(BaseModel):
    name:str = Field(...,description="Enter ypur name")
    age:int = Field(...,description="Enter ypour age")
    gender:str = Field(...,description="Enter your gender") 

class ResponseData(BaseModel):
    formated_data:str

@app.post("/info")
async def get_data(payload:InputData) -> ResponseData:
    formated_data = f"""
    Here  is your details:
    Your name: {payload.name.title()}
    Your age: {payload.age}
    Your gendr: {payload.gender} 
    """
    return {"Information":formated_data}
