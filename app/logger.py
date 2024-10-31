from logging import Logger, getLogger


logger: Logger = None


def get_logger() -> Logger:
    global logger
    if not logger:
        logger = getLogger("uvicorn.error")
    return logger
