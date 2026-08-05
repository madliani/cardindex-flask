from server.app import make_app
from server.blueprint import bp
from server.config import flask_host, flask_port, is_debug_mode, postgres_uri
from server.database import db, migrate

app = make_app(bp=bp, db=db, migrate=migrate, postgres_uri=postgres_uri)

if __name__ == "__main__":
    app.run(host=flask_host, port=flask_port, debug=is_debug_mode)
