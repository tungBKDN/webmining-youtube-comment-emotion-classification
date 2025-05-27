import os
import logging

class Logger:
   def __init__(self, log_file='./logs/log.txt'):
      os.makedirs(os.path.dirname(log_file), exist_ok=True)
      self.logger = logging.getLogger('AppLogger')
      self.logger.setLevel(logging.INFO)
      handler = logging.FileHandler(log_file, encoding='utf-8')
      formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
      handler.setFormatter(formatter)
      if not self.logger.handlers:
         self.logger.addHandler(handler)

   def info(self, message):
      self.logger.info(message)

   def warning(self, message):
      self.logger.warning(message)

   def error(self, message):
      self.logger.error(message)

# Usage example:
if __name__ == "__main__":
    logger = Logger()
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    print("Logging setup complete. Check the log file for messages.")