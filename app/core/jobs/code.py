from ...utils.logger import logger


def generator_standard_code(config):
    import time
    time.sleep(30)
    logger.info('config =======================================')
    print(config.__dict__)