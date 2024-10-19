from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from typing import Dict, Any
from qdrant_client.http import models
from search_success_videos.chain import chain as search_success_videos_chain
from starlette.requests import Request

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

def json_to_python_filter(json_filter: Dict[str, Any]) -> models.Filter:
    def parse_condition(condition: Dict[str, Any]) -> models.FieldCondition:
        key = condition['key']
        match_data = condition['match']
        
        if 'value' in match_data:
            match = models.MatchValue(value=match_data['value'])
        elif 'any' in match_data:
            match = models.MatchAny(any=match_data['any'])
        else:
            raise ValueError(f"Unsupported match type in condition: {condition}")
        
        return models.FieldCondition(key=key, match=match)

    must = [parse_condition(cond) for cond in json_filter.get('must', [])]
    should = [parse_condition(cond) for cond in json_filter.get('should', [])]

    return models.Filter(must=must or None, should=should or None)


async def config_modifier(config: Dict[str, Any], req: Request) -> Dict[str, Any]:
    print(config)
    body = await req.json()
    print(body)
    filter = config.get("configurable", {}).get("search-parameters", {}).get("filter")
    if filter:
        config["configurable"]["search-parameters"]["filter"] = json_to_python_filter(filter)
    # if "id" not in body:
    #     raise HTTPException(status_code=400, detail="Missing 'id' parameter")
    # document = await chat_config.get_document_by_id(body["id"])
    # if document is None:
    #     raise HTTPException(status_code=400, detail="Invalid 'id' parameter")
    # # set config configurable->search-parameters->filter->namespace" to document["namespace"] use setdefault
    # config.setdefault("configurable", {}).setdefault(
    #     "search-parameters", {}
    # ).setdefault("filter", {})["namespace"] = document["namespace"]
    # print("config:", config)
    return config


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


# Edit this to add the chain you want to add
add_routes(
    app,
    search_success_videos_chain,
    path="/search_success_videos_chain",
    playground_type="default",
    per_req_config_modifier=config_modifier,
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
