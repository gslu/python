import logging
import logging.config

logging.config.fileConfig("./logconf")

def test():
    logger = logging.getLogger("lgtest03")

    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')
    
if __name__ == '__main__':
    test()
