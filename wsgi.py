from app import app
import os

port = int(os.environ.get('PORT', 33507))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=port)