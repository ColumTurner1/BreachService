from dotenv import load_dotenv
import os
import yaml
import logging


class Core:
    """
    Handles configuration loading and logger setup.
    """

    def __init__(self, config_path: str = "config.yaml"):
        # Try loading api.env first, fallback to .env
        if os.path.exists("api.env"):
            load_dotenv(dotenv_path="api.env")
        else:
            load_dotenv()

        # Load config
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        # Retrieve API key from environment
        self.api_key = os.getenv("INTELX_API_KEY")
        if not self.api_key:
            raise EnvironmentError("INTELX_API_KEY not set in environment.")

        self.logger = self._setup_logger()

    @property
    def api_base_url(self) -> str:
        return self.config["api"]["base_url"]

    @property
    def timeout(self) -> int:
        return self.config["api"]["timeout"]

    @property
    def retry_attempts(self) -> int:
        return self.config["retry"]["attempts"]

    @property
    def retry_backoff(self) -> int:
        return self.config["retry"]["backoff_seconds"]

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("breach_tool")

        # Convert YAML log level string to logging constant
        log_level_str = self.config["logging"]["level"].upper()
        log_level = getattr(logging, log_level_str, logging.INFO)

        logger.setLevel(log_level)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        # File handler
        file_handler = logging.FileHandler(self.config["logging"]["file"])
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)

        # Prevent duplicate handlers if logger is reinitialised
        if not logger.handlers:
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        return logger

