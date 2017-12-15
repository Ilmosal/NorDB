import logging
import sys

class ErrorMessages():
    """
    Class that contains error messaging functionality of the program.

    Attributes
    """
    def __init__(self, verbosity = False, errorLogPath):
        self.verbosity = verbosity
        self.errorLogPath = errorLogPath
        self.logger = logging.getLogger(__name__)
        

    def throwErrorMessage(msg, cont):
        """
        Function for writing error messages to user with logging library.

        Args:
            msg(str): error message that will be thrown
        """
        logging.error(msg)

        if not cont:
            sys.exit(-1)
