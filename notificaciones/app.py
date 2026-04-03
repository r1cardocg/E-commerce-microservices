from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

from routes import bp

app = Flask(__name__)
app.register_blueprint(bp)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8005))
    app.run(host='0.0.0.0', port=port, debug=True)
    