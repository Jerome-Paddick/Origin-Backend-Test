from app.app_factory import create_app
from app.config import DefaultConfig

app = create_app(config=DefaultConfig)

# do some production specific things to the app
app.config['DEBUG'] = False