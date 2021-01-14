from logging import getLogger

def with_log(cls):
    setattr(cls, 'log', getLogger(f'{cls.__module__}.{cls.__qualname__}'))
    return cls
