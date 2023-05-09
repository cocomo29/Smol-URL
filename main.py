# Import the necessary libraries.
from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import random
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize the FastAPI app.
app = FastAPI()

# Initialize the Jinja2 template engine. We use jinja2 to write python code in html files.
templates = Jinja2Templates(directory="templates")

# Load the Firebase credentials. These credentials are used to authenticate the Firebase.
cred = credentials.Certificate('/path/to/serviceAccountKey.json') # You can get this file from the Firebase console by going to Project Settings > Service Accounts > Generate New Private Key.
# Initialize the Firebase Admin and provide the credentials as an argument.
firebase_admin.initialize_app(cred)
# Create a database client. db variable now represents the Firestore database.
db = firestore.client()

# Define a function to generate a random short URL.
def generateShortUrl():
    # Create a list of letters and numbers.
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    # Generate a short URL of 6 characters.
    return ''.join(random.choice(letters) for i in range(6))

def customShortUrl():pass # TODO

# Define a function to create a temporary object with the short URL and long URL.
def createTempObject(url):
    # Generate a short URL and store it in a variable.
    shortUrl = generateShortUrl()
    # Create a temporary object. This object will be used to save the short URL and long URL to Firestore.
    tempObj = {shortUrl: url}
    # Return the temporary object.
    return tempObj

# Define a function to save the short URL and long URL to Firestore.
def saveUrlToFirestore(shortUrl, longUrl):
    # Create a document reference in Firestore.
    docRef = db.collection(u'short_urls').document(shortUrl)
    # Set the document data.
    docRef.set({'long_url': longUrl})

# Define a function to get the long URL from Firestore.
def getUrlFromFirestore(shortUrl):
    # Create a document reference in Firestore.
    docRef = db.collection(u'short_urls').document(shortUrl)
    # Get the document data.
    doc = docRef.get()
    # If the document exists, return the long URL.
    if doc.exists:
        return doc.to_dict()['long_url']
    # Otherwise, return None.
    else:
        return None

# Define the `root` route.
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # Return the index.html template.
    return templates.TemplateResponse("index.html", {"request": request})

# Define the `shorten` route.
@app.post("/shorten", response_class=HTMLResponse)
async def shorten(request: Request, url: str = Form(...)):
    # Create a temporary object.
    tempObj = createTempObject(url)
    # Save the short URL and long URL to Firestore.
    for shortUrl, longUrl in tempObj.items():
        saveUrlToFirestore(shortUrl, longUrl)
    # Return the index template with the short URL.
    return templates.TemplateResponse("index.html", {"request": request, "short_url": f"/{shortUrl}"})

# Define the `redirectToUrl` route.
@app.get("/{shortUrl}", response_class=RedirectResponse)
async def redirectToUrl(request: Request, shortUrl: str):
    # Get the long URL from Firestore.
    longUrl = getUrlFromFirestore(shortUrl)
    # If the long URL is None, return an error message.
    if longUrl is None:
        return templates.TemplateResponse("index.html", {"request": request, "error_message": "Short URL not found."})
    # Otherwise, redirect to the long URL.
    else:
        return RedirectResponse(url=longUrl)
