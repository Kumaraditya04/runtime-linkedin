import logging
import sys

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    
    # Silence chatty third-party loggers if needed
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

setup_logging()
