import firebase_admin
from firebase_admin import credentials, firestore

# Initialize the FastAPI app.

# Initialize the Jinja2 template engine. We use jinja2 to write python code in html files.

# Load the Firebase credentials. These credentials are used to authenticate the Firebase.
cred = credentials.Certificate(r'api\v1\db\firebase\config.json') # You can get this file from the Firebase console by going to Project Settings > Service Accounts > Generate New Private Key.
# Initialize the Firebase Admin and provide the credentials as an argument.
firebase_admin.initialize_app(cred)
# Create a database client. db variable now represents the Firestore database.
db = firestore.client()

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