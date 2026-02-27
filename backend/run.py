import os
import logging
from app import create_app, db

logger = logging.getLogger(__name__)

env = os.getenv('FLASK_ENV', 'development')
app = create_app(env)

if __name__ == '__main__':
    if env != 'production':
        with app.app_context():
            db.create_all()
            logger.info('Database tables ensured (dev mode)')

    debug = env != 'production'
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=debug,
    )
