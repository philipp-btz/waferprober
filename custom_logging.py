'''

    Philipp Bartz 2025

    This file is part of the Velox project.

    If you want to get push notifications about errors, you can use the ntfy.sh service.
    (https://ntfy.sh/)

'''

# #####       Version 3.1       #####


import logging
import sys
import requests
from logging.handlers import RotatingFileHandler

class CustomLogger:
    CUSTOM_LEVELS = {
        'PATH': 15,
        'MEASUREMENT': 21,
        'LOWERING': 31,
        'FILE': 23,
        'QUIET': 24,
        'WAFERPROBER': 22,
    }

    CUSTOM_LEVEL_NAMES = {
        'DEBUG': '🐛 DEBUG',
        'INFO': 'ℹ️ INFO',
        'PATH': '🧭 PATH',
        'MEASUREMENT': '📏 MEASUREMENT',
        'LOWERING': '⬇️ LOWERING',
        'FILE': '📂 FILE',
        'QUIET': '🔇 QUIET',
        'WAFERPROBER': '🧪 WAFERPROBER',
        'WARNING': '⚠️ WARN',
        'ERROR': '❌ ERROR',
        'CRITICAL': '💥 CRITICAL',
    }

    COLOR_CODES = {
        'DEBUG': '\033[36m',
        'INFO': '\033[35m',
        'PATH': '\033[94m',
        'MEASUREMENT': '\033[92m',
        'LOWERING': '\033[91m',
        'FILE': '\033[96m',
        'QUIET': '\033[93m',
        'WAFERPROBER': '\033[92m',
        'WARNING': '\033[33m',
        'ERROR': '\033[31m',
        'CRITICAL': '\033[41m',
        'RESET': '\033[0m',
    }

    class CustomFormatter(logging.Formatter):
        def format(self, record):
            original_levelname = record.levelname
            display_name = CustomLogger.CUSTOM_LEVEL_NAMES.get(original_levelname, original_levelname)
            color = CustomLogger.COLOR_CODES.get(original_levelname, '')
            record.levelname = display_name
            formatted = super().format(record)
            record.levelname = original_levelname
            return f"{color}{formatted}{CustomLogger.COLOR_CODES['RESET']}"
    
    class NtfyHandler(logging.Handler):
        def __init__(self, topic_url):
            super().__init__(level=logging.CRITICAL)
            self.topic_url = topic_url

        def emit(self, record):
            try:
                message = self.format(record)
                requests.post(self.topic_url, data=message.encode("utf-8"), timeout=30)
            except Exception as e:
                # Optionally log failures in sending to ntfy
                print(f"Failed to send ntfy.sh notification: {e}")
            
    @staticmethod
    def setup_logger(*, name="custom_logger", log_file="custom_levels.log", level=logging.DEBUG):
        # Register custom levels and methods
        for level_name, level_num in CustomLogger.CUSTOM_LEVELS.items():
            logging.addLevelName(level_num, level_name)

            def make_level_method(level):
                def log_for_level(self, message, *args, **kwargs):
                    if self.isEnabledFor(level):
                        self._log(level, message, args, **kwargs)
                return log_for_level

            setattr(logging.Logger, level_name.lower(), make_level_method(level_num))

        logger = logging.getLogger(name)
        logger.setLevel(level)

        if logger.hasHandlers():
            return logger  # Prevent duplicate handlers

        # Console handler with color
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(30)  # Only show logs with level >= 30
        console_handler.setFormatter(CustomLogger.CustomFormatter('%(levelname)s - %(message)s'))

        # File handler without color
        file_handler = RotatingFileHandler(log_file, maxBytes=8*1024*1024, backupCount=500)     ## Adjust Values Here if you want bigger/smaller log files
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        # ntfy.sh handler
        NTFY_TOPIC = "https://ntfy.sh/WaferproberNotifications--------EdG2HGYuxMaNoZf3eUNRWsiKie"
        ntfy_handler = CustomLogger.NtfyHandler(NTFY_TOPIC)
        ntfy_handler.setLevel(logging.CRITICAL)
        ntfy_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.addHandler(ntfy_handler)

        return logger
    

