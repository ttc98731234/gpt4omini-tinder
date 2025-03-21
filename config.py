
"""
Configuration settings for the ChatGPT Tinder Bot
"""

# OpenAI API settings
DEFAULT_MODEL_ENGINE = "gpt-4o-mini"  # Default to GPT-4o Mini
DEFAULT_IMAGE_SIZE = "1024x1024"      # DALL-E image size
DEFAULT_IMAGE_QUALITY = "standard"    # DALL-E image quality

# ChatGPT settings
DEFAULT_SYSTEM_MESSAGE = "You are a helpful assistant."
DEFAULT_TEMPERATURE = 0.7             # Controls randomness (0-1)

# Scheduler settings
SCHEDULER_INTERVAL_MINUTES = 5        # How often to check for new messages

# Logging settings
LOG_LEVEL = "INFO"                    # DEBUG, INFO, WARNING, ERROR, CRITICAL
