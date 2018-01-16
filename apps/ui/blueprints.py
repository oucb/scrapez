from apps.ui.home import home as home_bp
from apps.ui.links import links as links_bp
from apps.ui.videos import videos as videos_bp
from apps.ui.downloads import downloads as downloads_bp
from apps.ui.chat import chat as chat_bp

BLUEPRINTS = [
    (home_bp, '/'),
    (links_bp, '/links'),
    (videos_bp, '/videos'),
    (downloads_bp, '/downloads'),
    (chat_bp, '/chat'),
]
