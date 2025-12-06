import logging

logger = logging.getLogger("payment_api")
logger.setLevel(logging.INFO)

# Prevent duplicate handlers if module is imported multiple times
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    logger.addHandler(handler)
