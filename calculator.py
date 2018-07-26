"""
This code includes two solutions for the mathematical operations:
1.) functions for each mathematical operation that are called by the dict funcs
2.) each mathematical operation as a value in the dict funcs
"""

from functools import reduce
import traceback


def index(*args):
    page_text = str("""<h1>WSGI Calculator HW4</h1>
    <p>To add numbers follow this logic in URL: http://localhost:8080/add/23/42 =>65</p>
    <p>To subtract numbers follow this logic in URL: http://localhost:8080/subtract/23/42 =>-19</p>
    <p>To multiply numbers follow this logic in URL: http://localhost:8080/multiply/3/5 =>15</p>
    <p>To divide numbers follow this logic in URL: http://localhost:8080/divide/22/11 =>2</p>
    <p>Any number of arguments may be provided in URL i.e. add/24/5/7/9/10</p>
    """)

    return page_text


def add(*args):
    """Returns a STRING with the sum of the arguments"""

    numbers = [int(i) for i in args]
    result = str(sum(numbers))

    return result


def subtract(*args):
    """Returns a STRING with the difference of the arguments"""

    numbers = [int(i) for i in args]
    result = str(reduce(lambda x, y: x - y, numbers))

    return result


def multiply(*args):
    """Returns a STRING with the product of the arguments"""

    numbers = [int(i) for i in args]
    result = str(reduce(lambda x, y: x * y, numbers))

    return result


def divide(*args):
    """Returns a STRING with the quotient of the arguments"""

    numbers = [int(i) for i in args]
    result = str(reduce(lambda x, y: x / y, numbers))

    return result


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    funcs = {
        '': index,
        #'add': add,
        'add': (lambda *args: str(sum([int(i) for i in args]))),
        #'subtract': subtract,
        'subtract': (lambda *args: str(reduce(lambda x, y: x - y, [int(i) for i in args]))),
        #'multiply': multiply,
        'multiply': (lambda *args: str(reduce(lambda x, y: x * y, [int(i) for i in args]))),
        #'divide': divide,
        'divide': (lambda *args: str(reduce(lambda x, y: x / y, [int(i) for i in args]))),
    }

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = '200 OK'
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = '500 Internal Server Error'
        body = '<h1>Internal Server Error</h1>'
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
