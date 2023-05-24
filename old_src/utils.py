import multiprocessing


def dump_queue(queue: multiprocessing.Queue):
    """
    Empties all pending items in a queue and returns them in a list.
    """
    result = []

    while not queue.empty():
        result.append(queue.get())
    return result
