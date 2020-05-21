from functools import reduce


def threshold_time(data, threshold):
    return [d for d in data if d['time'] > threshold]


def module_path(data, path):
    return [d for d in data if path in d['file_path']]


def app_only(data, worker):
    return [d for d in data if worker.wsgi.root_path in d['file_path']]


def compose(fns):
    return lambda data: reduce(lambda x, y: y(x), fns, data)
