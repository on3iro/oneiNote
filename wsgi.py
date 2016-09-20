from oneiNote.app import create_app
from oneiNote.settings import ProdConfig

application = create_app(ProdConfig)
