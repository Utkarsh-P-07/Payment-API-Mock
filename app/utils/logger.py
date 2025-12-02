import logging

logger = logging.getLogger("payment_api")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))

logger.addHandler(handler)
