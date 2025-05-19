import logging

class Logger:
    _instance = None

    @staticmethod
    def get_logger():
        if Logger._instance is None:
            Logger._instance = Logger._init_logger()
        return Logger._instance

    @staticmethod
    def _init_logger():
        logger = logging.getLogger("ERAT")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            ch = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)s] %(message)s')
            ch.setFormatter(formatter)
            logger.addHandler(ch)
        return logger
