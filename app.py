import logging
import os

import dotenv

import bva

dotenv.load_dotenv()

bva.initialize_logging(stdout_level=logging.getLevelName(os.getenv("LOGGING_LEVEL", "INFO")))

app = bva.create_app()

if __name__ == '__main__':
    app.run()
