import sys
import traceback

def install_global_exception_hook(logger):
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.error(
            "Unhandled exception",
            extra={
                "exc_type": str(exc_type),
                "exc_value": str(exc_value),
                "traceback": "".join(traceback.format_exception(exc_type, exc_value, exc_traceback)),
            }
        )
        # Still raise for visibility/testing
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
    sys.excepthook = handle_exception