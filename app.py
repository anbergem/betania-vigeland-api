import os

import bva
import dotenv
import logging

dotenv.load_dotenv()

app = bva.create_app()

if __name__ == '__main__':
    bva.initialize_logging(stdout_level=logging.getLevelName(os.getenv("LOGGING_LEVEL", "INFO")))
    app.run(debug=True)