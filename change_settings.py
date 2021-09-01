# TODO: make this a full GUI app
# Right now it just sets up the DB.

from db_gui_app.db_classes import engine, Base

Base.metadata.create_all(engine)