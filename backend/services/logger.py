import logging
import json
import sys



class JsonFormatter(logging.Formatter):

    def format(self,record):
        log_obj = { 
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "service": record.name,
            "message": record.getMessage()
        }

        if record.exc_info:
            log_obj['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_obj)
