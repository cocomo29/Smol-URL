# Necessary imports
from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import random

# This is the FastAPI app object, just remember it as a fudamental part of FastAPI.
app = FastAPI()

# This is the Jinja2 template engine. We use jinka2 to write python code in html files.
templates = Jinja2Templates(directory="templates")

# This is the path to the file that stores the shortened URLs. | soon wil be replaece with a database
data = "shortened_urls.txt"

# This function loads the shortened URLs from the file `data`.
def loadShortenedUrls():
    # Try to open the file `data`.
    try:
        with open(data, "r") as f:
            # Return a dictionary that maps short URLs to their corresponding long URLs.
            return dict(line.strip().split(",") for line in f)
    # If the file `data` does not exist, return an empty dictionary.
    except FileNotFoundError:
        return {}

# This function saves the shortened URLs to the file `data`.
def saveShortenedUrls(shortened_urls):
    # Open the file `data` in write mode.
    with open(data, "w") as f:
        # Write the shortened URLs to the file.
        for short_url, long_url in shortened_urls.items():
            f.write(f"{short_url},{long_url}\n")

# This is a dictionary that maps short URLs to their corresponding long URLs.
shortUrls = loadShortenedUrls()

# This function generates a random six-character short URL.
def generateShortUrl():
    # This is a string of all the possible characters that can be used in a short URL.
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    # Return a random six-character short URL.
    return ''.join(random.choice(letters) for i in range(6))

def customShortUrl():pass # TODO

# This function renders the index.html in templates directory.
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # Return the index.html template with the request object as the context.
    return templates.TemplateResponse("index.html", {"request": request})

# This function shortens a long URL and returns a HTML response with the shortened URL.
@app.post("/shorten", response_class=HTMLResponse)
async def shorten(request: Request, url: str = Form(...)):
    # Generate a random short URL.
    short_url = generateShortUrl()

    # Add the short URL to the dictionary of short URLs.
    shortUrls[short_url] = url

    # Save the dictionary of short URLs to the file `data`.
    saveShortenedUrls(shortUrls)

    # Return the index.html template with the short URL as the context.
    return templates.TemplateResponse("index.html", {"request": request, "short_url": f"/{short_url}"})

# This function redirects the request to the long URL associated with the short URL.
@app.get("/{short_url}", response_class=RedirectResponse)
async def redirect_to_url(request: Request, short_url: str):
    # If the short URL is not in the dictionary of short URLs, return an error message.
    if short_url not in shortUrls:
        return templates.TemplateResponse("index.html", {"request": request, "error_message": "The URL you requested does not exist."})

    # Redirect the request to the long URL associated with the short URL.
    return RedirectResponse(url=shortUrls[short_url])
