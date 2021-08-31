# Accounts Receivable Project for EVIT Year 2 Coding
GUI application for managing a database with customers, products and sales.

## Prerequisites
All packages needed are in `requirements.txt`.
* Python version must be 3.8+
* SQLAlchemy
* toml
* If you are planning to interface with a database other than SQLite, make sure to setup
  the database itself and install the package(s) necessary (for example, psycopg2 for PostgreSQL)

## Setup
The default settings are for a SQLite memory database, with a sample window title.  
There is an included graphical utility (`change_settings.py`) which will also set up the database.

## Usage
* To run application: `python3 -m db_gui_app`
* To run settings utility: `python3 change_settings.py`
