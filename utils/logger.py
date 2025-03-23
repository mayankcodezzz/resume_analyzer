import logging
import os

def setup_logger(name, log_file, level=logging.DEBUG):
    """Set up a logger with console and file handlers."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Ensure logs directory exists
    log_dir = os.path.dirname(log_file)
    os.makedirs(log_dir, exist_ok=True)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers (only if not already added)
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger