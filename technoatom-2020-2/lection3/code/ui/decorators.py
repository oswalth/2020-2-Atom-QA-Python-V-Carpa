import time


def wait(method, timeout=1, err=Exception, check=False, interval=1, **kwargs):
    start = time.time()
    while time.time() < start + timeout:
        try:
            result = method(**kwargs)
            if check:
                if result:
                    return result
            else:
                return result
        except err as exc:
            pass
        time.sleep(interval)

    raise Exception(f"{method.__name__}")