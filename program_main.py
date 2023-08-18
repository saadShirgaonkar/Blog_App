from uvicorn import run

if __name__ == "__main__":
    run("app.main:app", port=8000,reload=True)