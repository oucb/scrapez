from apps.ui.files import files as files_bp
from apps.ui.links import links as links_bp
from apps.ui.videos import videos as videos_bp
from apps.ui.downloads import downloads as downloads_bp
from apps.ui.chat import chat as chat_bp

BLUEPRINTS = [
    (files_bp, '/files'),
    (links_bp, '/links'),
    (videos_bp, '/videos'),
    (downloads_bp, '/downloads'),
    (chat_bp, '/chat'),
]
