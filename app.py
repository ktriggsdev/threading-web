from flask import Flask, request, render_template
from time import time
from threading import Thread


class InvalidThreadChoice(Exception):
    pass


COUNT = 50000000


def countdown(n):
    """ function used to countdown from n:
    n -> int: the number being counted down from
    while n > 0 -> n -= 1
    """
    while n > 0:
        n -= 1


def single_thread():
    """function used to define a single thread:
    start -> time()
    countdown(COUNT: int)
    end -> time()
    """
    start = time()
    countdown(COUNT)
    end = time()
    execution_time = end - start
    return execution_time


def multi_thread():
    """function used to define a multithread:
    t1 -> Thread(target: countdown, args: COUNT // 2)
    t2 -> Thread(target: countdown, args: COUNT // 2)
    start -> time()
    t1 -> start() -> starts thread 1
    t2 -> start() -> starts thread 2
    t1 -> join() -> joins thread 1
    t2 -> join() -> joins thread 2
    end -> time()
    """
    t1 = Thread(target=countdown, args=(COUNT // 2,))
    t2 = Thread(target=countdown, args=(COUNT // 2,))
    start = time()
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    end = time()
    execution_time = end - start
    return execution_time


app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/start_threads', methods=['POST'])  # Handle thread choice
def start_threads():
    count_str = request.form.get('COUNT')
    choice = request.form.get('choice')  # Get user's choice
    try:
        count = int(count_str)
        if count <= 0:
            raise ValueError("Count must be a positive integer")

        if choice == '1':
            single_thread()
        elif choice == '2':
            multi_thread()
        else:
            raise InvalidThreadChoice("Invalid choice")
    except InvalidThreadChoice as e:
        return render_template('error.html', error=e)
    if choice == '2':
        return render_template('results.html', execution_type="Multithreading",
                               execution_time=multi_thread())
    elif choice == '1':
        return render_template('results.html', execution_type="Single Thread",
                               execution_time=single_thread())


if __name__ == '__main__':
    app.run()
