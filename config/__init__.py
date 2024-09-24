import os

# Get the environment variable ENV, default to 'dev'
env = os.getenv('ENV', 'dev')

if env == 'dev':
    from .dev import config
elif env == 'prod':
    from .prod import config
else:
    raise ValueError(f"Unknown environment: {env}")
