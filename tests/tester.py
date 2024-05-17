from tools.error_logger import ErrorLogger

# Create an instance of the ErrorLogger
logger = ErrorLogger()

try:
    # This code will raise a NameError since variable 'undefined_var' is not defined
    print(undefined_var)
except Exception as e:
    # Log the error using the ErrorLogger
    logger.log_error_from_exception(applicant_id=1, applicant_ip='127.0.0.1', page='test_page', exception=e)