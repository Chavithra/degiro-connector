class DeGiroConnectionError(ConnectionError):
    """Exception raised for data validation errors."""
    def __init__(self, message, error_details):
        """
        Initializes the exception with a message and a structure of error details.

        Args:
            message (str): The error message.
            error_details (LoginError): The login error details
        """
        super().__init__(message)
        self.error_details = error_details

class MaintenanceError(DeGiroConnectionError):
    """Exception raised when DeGiro is in maintenance mode."""
    def __init__(self, message, error_details):
        """
        Initializes the exception with a message and a structure of error details.

        Args:
            message (str): The error message.
            error_details (LoginError): The login error details
        """
        super().__init__(message, error_details)

class CaptchaRequiredError(DeGiroConnectionError):
    """Exception raised when DeGiro requires a captcha."""
    def __init__(self, message, error_details):
        """
        Initializes the exception with a message and a structure of error details.

        Args:
            message (str): The error message.
            error_details (LoginError): The login error details
        """
        super().__init__(message, error_details)