from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import time
#imports the ThreadPoolExecutor class from the concurrent.futures module
#ThreadPoolExecutor is used to manage a pool of threads, where each thread can execute a task asynchronously
#have multiple tasks to execute, you can specify how many threads the executor should manage. The threads will execute tasks in parallel

#with statement ensures that the executor is properly initialized and cleaned up
#When the block inside the with statement is completed, it automatically shuts down the executor, meaning it cleans up resources (threads in this case).
#max_workers=1 specifies that the executor will only use one thread for executing tasks. So, it will run tasks sequentially, one after another
#Using one worker here means there’s no parallelism involved; only one task can be processed at a time
with ThreadPoolExecutor(max_workers=1) as executor:
    #executor.submit schedules the callable pow (Python's built-in power function) to be executed asynchronously in the background thread
    #submit returns a Future object, which represents the execution of the pow(323, 1235) function. This object will eventually contain the result once the computation is done.
    #The Future object returned by submit is like a placeholder for the result. You can check if the task is complete or wait for the result to be available.
    future = executor.submit(pow, 323, 1235)
    #future.result() is used to block the program execution until the task (pow(323, 1235)) completes. When the computation finishes, result() will return the result of the function.
    print(future.result())


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Function to apply
#A simple function that returns the square of x, but it sleeps for 1 second to simulate a "heavy" operation
def square(x):
    time.sleep(1)  # simulate a time-consuming task
    return x * x

# List of numbers to square
numbers = [1, 2, 3, 4, 5]

# Using ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=3) as executor:
    # map applies 'square' to each element in 'numbers' asynchronously
    #'square' is fn
    #'numbers' is the iterable
    #starts working on multiple numbers at the same time (because of threading)
    #Because max_workers=3, it can process up to 3 numbers simultaneously
    results = executor.map(square, numbers)

    # results is an iterator — we can loop through it to get the results
    for result in results:
        print(result)

#behavior:
    #Since we set max_workers=3, the executor will:
        #Start squaring 3 numbers immediately (say, 1, 2, and 3)
        #After about 1 second, those 3 results are ready
        #Then it will move to 4 and 5
        #So the total time will be about 2 seconds, not 5 seconds

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Example 3:
    #using ProcessPoolExecutor and chuncksize

import os

# Function to simulate a CPU-heavy task
#prints the current process ID (os.getpid()) to show you which process is working on each number.
def compute(x):
    print(f"Process {os.getpid()} is computing {x}...")
    time.sleep(1)  # simulate heavy computation
    return x * x

# Large list of numbers
numbers = list(range(10))

# Using ProcessPoolExecutor
with ProcessPoolExecutor(max_workers=4) as executor:
    # map applies 'compute' to each element in 'numbers'
    # Setting chunksize=2 means each process gets 2 numbers at a time
    results = executor.map(compute, numbers, chunksize=2)

    for result in results:
        print(f"Result: {result}")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Example 4:
    #downloading contents from URLS in parallel

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

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Example 5
    #ProcessPoolExecutor
    #Sqauring an array of numbers
    #demonstrating each argument of concurrent.futures.ProcessPoolExecutor()

import concurrent.futures
import os
import time
import multiprocessing

# This function will be run at the start of each process
def initializer_function(worker_name):
    # Print the process ID and the worker name to indicate it's initializing
    print(f"[{os.getpid()}] Initializing worker: {worker_name}")

# This is the task each process will do
def work(x):
    # Print the process ID and the number it's working on
    print(f"[{os.getpid()}] Working on: {x}")
    
    # Simulate a slow task by sleeping for 1 second
    time.sleep(1) 
    
    # Return the square of the number as the result
    return x * x

# Create a custom context that uses "spawn" method
mp_ctx = multiprocessing.get_context('spawn')

# Create the process pool
with concurrent.futures.ProcessPoolExecutor(
    max_workers=2,  # Only 2 worker processes will run concurrently
    mp_context=mp_ctx,  # Set the multiprocessing context to use the "spawn" method
    initializer=initializer_function,  # The function to run when each worker process is initialized
    initargs=('WorkerProcess',),  # Pass 'WorkerProcess' as an argument to the initializer
    max_tasks_per_child=3  # After each worker completes 3 tasks, it will restart with a fresh worker
) as executor:
    
    # Submit tasks to the worker processes. This assigns numbers 0–5 to be processed by workers
    results = list(executor.map(work, range(6)))  # Use executor.map to run the 'work' function on numbers 0 to 5

# Print the results after all tasks are done
print("Results:", results)

# Step-by-step what’s happening:
# - initializer_function(worker_name) is called once for each worker process when it starts.
# - It prints which process is initializing.
#
# - work(x) is the real "job" function:
#   - It prints which process is handling which number.
#   - It sleeps for 1 second to pretend it's a slow task.
#   - Then it returns the square of the number.
#
# - mp_context forces processes to be created using the "spawn" method (like Windows style — clean new process).
#
# - ProcessPoolExecutor settings:
#   - max_workers=2: Only 2 processes at a time.
#   - initializer=initializer_function: Run initializer when a worker starts.
#   - initargs=('WorkerProcess',): Pass 'WorkerProcess' as the argument to the initializer.
#   - max_tasks_per_child=3: After doing 3 tasks, the process will restart with a fresh one.
#
# - executor.map(work, range(6)): Assigns numbers 0–5 to the workers.


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Example 6
#using ProcessPoolExecutor

import concurrent.futures
import math

PRIMES = [
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419]

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

def main():
    with concurrent.futures.ProcessPoolExecutor() as executor:

        #for each "number" in PRIMES
        #"prime" is the boolean value of "is_prime" on that number
        #zip(PRIMES, executor.map(...)) pairs each original number with its corresponding result (True/False) from the is_prime() function.
        for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
            print('%d is prime: %s' % (number, prime))

if __name__ == '__main__':
    main()




