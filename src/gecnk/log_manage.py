import logging
import logging.handlers
import datetime


def __get_logger():
    """로거 인스턴스 반환
    """

    __logger = logging.getLogger('logger')
    log_file = './logs/logfile_{:%Y%m%d}.log'.format(datetime.datetime.now())

    # 로그 포멧 정의
    formatter = logging.Formatter(
        'BATCH##AWSBATCH##%(levelname)s##%(asctime)s##%(message)s >> @@file::%(filename)s@@line::%(lineno)s')
    # 스트림 핸들러 정의
    stream_handler = logging.StreamHandler()
    # 각 핸들러에 포멧 지정
    stream_handler.setFormatter(formatter)
    # 파일 핸들러
    #filehandler = logging.FileHandler(log_file, encoding='utf-8')
    # filehandler.setFormatter(formatter)
    # RotatingFileHandler
    log_max_size = 10 * 1024 * 1024  # 10MB
    log_file_count = 20
    rotatingFileHandler = logging.handlers.RotatingFileHandler(
        filename=log_file,
        maxBytes=log_max_size,
        backupCount=log_file_count
    )
    rotatingFileHandler.setFormatter(formatter)
    __logger.addHandler(rotatingFileHandler)

    # __logger.addHandler(filehandler)
    # 로거 인스턴스에 핸들러 삽입
    # __logger.addHandler(stream_handler)
    # 로그 레벨 정의
    __logger.setLevel(logging.INFO)

    return __logger
