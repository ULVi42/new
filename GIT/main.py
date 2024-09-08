from fastapi import FastAPI
import router
import uvicorn

app=FastAPI(docs_url="/docs")

app.include_router(router.router)

if __name__=="__main":
    uvicorn.run("main:app",host="127.0.0.1",port="8080",reload=True)
    