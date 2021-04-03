import os
from app import create_app

config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
