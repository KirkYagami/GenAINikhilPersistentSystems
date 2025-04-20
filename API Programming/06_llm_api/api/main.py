from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from llm.models import LLM

app = FastAPI(
    title="LLM API",
    description="API for interacting with various LLM providers",
    version="1.0.0"
)


@app.get('/')
def index():
    return {'Welcome to llms api'}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    name: str = Field(..., )
    email: str
    age: int


@app.get('/getuser')
def getuser(id:int):

    return 

class CompletionRequest(BaseModel):
    system_prompt: str = Field(..., description="System prompt for context setting")
    user_prompt: str = Field(..., description="User prompt for the model")
    max_tokens: int = Field(1024, description="Maximum tokens to generate")
    temperature: float = Field(0.7, description="Temperature for generation")

class CompletionResponse(BaseModel):
    model: str
    content: str

@app.get("/models", response_model=List[str])
async def list_models():
    return LLM.all_model_names()

@app.post("/completion/{model_name}", response_model=CompletionResponse)
async def create_completion(model_name: str, request: CompletionRequest):
    try:
        llm = LLM.for_model_name(model_name, temperature=request.temperature)
        
        response = llm.send(
            system_prompt=request.system_prompt,
            user_prompt=request.user_prompt,
            max_tokens=request.max_tokens
        )
        
        return CompletionResponse(model=model_name, content=response)
    except KeyError:
        available_models = LLM.all_model_names()
        raise HTTPException(
            status_code=404, 
            detail=f"Model '{model_name}' not found. Available models: {', '.join(available_models)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/providers")
async def list_providers():
    providers = {}
    model_map = LLM.model_map()
    
    for model_name, llm_class in model_map.items():
        provider = llm_class.__name__
        if provider not in providers:
            providers[provider] = []
        providers[provider].append(model_name)
    
    return providers


