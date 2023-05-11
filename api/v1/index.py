from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from ...Shortner.main import *
from .db.firebase.db import *

app = FastAPI()

# Define the `root` route.
@app.get("/", response_class=HTMLResponse)
def root():
    return {"message": "Hello World"}


# Define the `shorten` route.
@app.post("/shorten")
def shorten(request: Request, url: str = Form(...)):
    # Create a temporary object.
    tempObj = createTempObject(url)
    # Save the short URL and long URL to Firestore.
    for shortUrl, longUrl in tempObj.items():
        saveUrlToFirestore(shortUrl, longUrl)
    # Return the index template with the short URL.
    return {"request": request, "short_url": f"/{shortUrl}"}

# Define the `redirectToUrl` route.
@app.get("/{shortUrl}", response_class=RedirectResponse)
def redirectToUrl(request: Request, shortUrl: str):
    # Get the long URL from Firestore.
    longUrl = getUrlFromFirestore(shortUrl)
    # If the long URL is None, return an error message.
    if longUrl is None:
        return {
            "message": "The short URL doesn't exist."
        }
    # Otherwise, redirect to the long URL.
    else:
        return RedirectResponse(url=longUrl)