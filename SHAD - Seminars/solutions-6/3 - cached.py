import functools


def cached(function):
    cached_results = {}

    @functools.wraps(function)
    def implementation(*args, **kwargs):

        kwargs_key = tuple(sorted(kwargs.items(), key=lambda x: x[0]))
        full_args_key = (args, kwargs_key)

        if full_args_key not in cached_results:
            result = function(*args, **kwargs)
            cached_results[full_args_key] = result
        return cached_results[full_args_key]

    return implementation


@cached
def f(a, b):
    print a, b
    return a + b


def main():
    print f(1, 2)
    print f(1, 2)


if __name__ == '__main__':
    main()
