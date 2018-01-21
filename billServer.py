from Bill import app
from os import environ

if __name__ == '__main__':
    app.run('0.0.0.0', port=int(environ.get('PORT', 5000)), debug=False, threaded=True)