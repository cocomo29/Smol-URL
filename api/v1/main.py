from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from Shortner.main import createTempObject
from .firebase.db import saveUrlToFirestore, getUrlFromFirestore
from fastapi.middleware.cors import CORSMiddleware
from typing import Any,Dict

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
# Define the `root` route.
@app.get("/")
async def root():
    # Return the index.html template.
    return {
        "hwllo":"wprd"
    }

# Define the `shorten` route.
@app.post("/shorten")
def shorten( url:  Dict[Any, Any]):
    # Create a temporary object.
    tempObj = createTempObject(url)
    # Save the short URL and long URL to Firestore.
    for shortUrl, longUrl in tempObj.items():
        saveUrlToFirestore(shortUrl, longUrl)
    # Return the index template with the short URL.
    return {"short_url": f"/{shortUrl}"}

# Define the `redirectToUrl` route.
@app.get("/{shortUrl}")
async def redirectToUrl(request: Request, shortUrl: str):
    # Get the long URL from Firestore.
    longUrl = getUrlFromFirestore(shortUrl)
    # If the long URL is None, return an error message.
    if longUrl is None:
        return {
            "meesage":"eror"
        }
    # Otherwise, redirect to the long URL.
    else:
        return {
            "url":longUrl
        }
