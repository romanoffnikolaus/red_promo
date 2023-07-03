def decorator(num):
    def inner_decor(func):
        def wrapper():
            for i in range(num):
                func()
        return wrapper
    return inner_decor

@decorator(4)
def hello():
    print('hello')

hello()





import time

def benchmark(func):
    def wrapper():
        start = time.time()
        func()
        finish = time.time()
        print(f'Время выполнения: {finish - start} секунд.')
    return wrapper



@benchmark 
def fetch_webpage(): 
  import requests 
  webpage = requests.get('https://google.com')  

fetch_webpage()