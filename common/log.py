import logging

logger = logging.getLogger('xunlei')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('log.log',encoding='utf-8')
fh.setLevel(logging.INFO)

# ch = logging.StreamHandler()
# ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# ch.setFormatter(formatter)

logger.addHandler(fh)