import logging
from pathlib import Path


class LoggerConfiguration:

    def __init__(self, filename, level=logging.DEBUG):
        """
        Constructor to initialize the logger configuration.
        :param filename: filename to log to
        :param level: level to log at
        """
        self.filename = filename
        self.level = level
        self.configure_logger(filename,level)

    @staticmethod
    def configure_logger(filename, level):
        """
        Configure the root logger to overwrite the log file on each run.
        """
        log_file_path = Path(__file__).parent / filename

        # Remove any existing handlers if already configured
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        # Create and set file handler with 'write' mode
        file_handler = logging.FileHandler(log_file_path, mode='w')
        file_handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Configure the root logger
        logging.basicConfig(level=level, handlers=[file_handler])

    @staticmethod
    def get_logger(name=None):
        """
        Class method to Get a logger with the given name.
        """
        return logging.getLogger(name)

    @staticmethod
    def close_loggers():
        """
        Class Method to Close and remove all handlers from the root logger.
        """
        for handler in logging.root.handlers[:]:
            handler.close()
            logging.root.removeHandler(handler)
