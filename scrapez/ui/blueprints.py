from home import home as home_bp
from links import links as links_bp
from videos import videos as videos_bp
from downloads import downloads as downloads_bp
from chat import chat as chat_bp

BLUEPRINTS = [
    (home_bp, '/'),
    (links_bp, '/links'),
    (videos_bp, '/videos'),
    (downloads_bp, '/downloads'),
    (chat_bp, '/chat'),
]
