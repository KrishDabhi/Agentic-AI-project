import logging
import os
from logging.handlers import RotatingFileHandler

def get_logger(name: str = "esg_monitor") -> logging.Logger:
    """
    Create and configure a logger with both console and file output.
    
    Args:
        name: Name of the logger (typically the module name).
        
    Returns:
        Configured Logger instance.
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # Set default level
    
    # Avoid adding multiple handlers if already configured
    if logger.handlers:
        return logger

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Create file handler (rotating logs)
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)  # Ensure logs directory exists
    log_file = os.path.join(log_dir, f"{name}.log")
    
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5*1024*1024,  # 5 MB per file
        backupCount=5           # Keep 5 backup files
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger