from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from search_success_videos.chain import chain as search_success_videos_chain

app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


# Edit this to add the chain you want to add
add_routes(
    app,
    search_success_videos_chain,
    path="/search_success_videos_chain",
    playground_type="default",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
