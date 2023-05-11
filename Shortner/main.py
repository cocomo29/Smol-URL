# Import the necessary libraries.
import random


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




