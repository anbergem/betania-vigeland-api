import bva
import dotenv

dotenv.load_dotenv()

app = bva.create_app()

if __name__ == '__main__':
    app.run()