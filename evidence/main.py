
import uvicorn
from fastapi import FastAPI
from evidence.routers import groups, locations, people, tags, places

if __name__ == "__main__":

    app = FastAPI()
    app.include_router(groups.router)
    app.include_router(people.router)
    app.include_router(tags.router)
    app.include_router(places.router)
    app.include_router(locations.router)

    uvicorn.run(app, host="0.0.0.0", port=8181)


