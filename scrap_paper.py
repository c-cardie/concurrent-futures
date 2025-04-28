import concurrent.futures
#concurrent.futures: lets us run things asynchronously (in parallel) using threads or processes
import urllib.request
#urllib.request: lets us download data from the web (like making a web browser request).

#A list called URLS containing 5 different website addresses.
#One of them (nonexistent-subdomain.python.org) doesn't actually exist 
# — we'll see an error when we try to fetch it!
URLS = ['http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://nonexistent-subdomain.python.org/']

#Define a function load_url that
    #Opens a given URL with a timeout (max seconds to wait)
    #Downloads all the page content (conn.read())
    #Returns the content (which is bytes, not text yet)
def load_url(url, timeout):

    #urllib.request.urlopen(url, timeout=timeout)
        #This opens a connection to the given website URL
            #"Hey website, give me your homepage!"
    #timeout=timeout means:
        #"Wait up to this many seconds for the website to respond."
        #If it takes too long, cancel and raise an error
        #It returns a connection object (let’s call it conn).
    #"with"
        #managing the connection resource safely
        # automatically closes the connection when you are done
    #"as conn"
        #gives the connection object a temporary name: conn
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()

#Create a ThreadPoolExecutor:
    #Up to 5 worker threads can run at the same time
    #executor is the object we’ll use to submit tasks
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    
    #For each url in the URLS list
        #Submit a task to executor to run load_url(url, 60)
            #This is asynchronous: they all start loading at the same time (roughly)
            #submit() immediately returns a Future object, which represents the ongoing task
    #Create a dictionary future_to_url
        #future -> url
    future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}

    #Go through the futures as they finish (not necessarily in the order we started them!)
    #as_completed() yields each future as soon as it’s done — perfect for seeing results immediately
    for future in concurrent.futures.as_completed(future_to_url):

        #Look up which URL this future was responsible for
        url = future_to_url[future]

        #Try to get the result of the future
        try:

            #Gives the returned page data if successful
            #Raise an exception (e.g., timeout, connection error) if something went wrong
            data = future.result()

        #If the task failed, catch the exception and print
            #The URL that failed
            #The specific error message
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))

        #If there was no error, print
            #The URL
            #How big the page was in bytes (length of downloaded data)
        else:
            print('%r page is %d bytes' % (url, len(data)))

print(future_to_url)