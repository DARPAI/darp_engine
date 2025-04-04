import logging

from mcp_server.src.settings import settings

logger = logging.getLogger("registry_mcp")
logger.setLevel(settings.log_level)

formatter = logging.Formatter("[%(asctime)s][%(name)s][%(levelname)s]: %(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

settings.log_dir.mkdir(parents=True, exist_ok=True)
file_handler = logging.FileHandler(settings.log_dir / "registry_mcp.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
