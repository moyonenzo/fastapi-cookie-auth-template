import src.models as models
from src.app import app
from src.database import engine

models.Base.metadata.create_all(bind=engine)
