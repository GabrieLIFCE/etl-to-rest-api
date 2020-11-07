from api.app_restx import app
from data_extraction.data_extractor import populate_database

if __name__ == '__main__':
    populate_database()
    app.run(port=5000, debug=True)
