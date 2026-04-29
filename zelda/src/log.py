import logging

def setup_logging():
    file_handler = logging.FileHandler('log.log', 'w', 'utf-8')
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[file_handler])
    logger = logging.getLogger(__name__)
    logger.log(logging.INFO, 'Initialized Logging successfully')
