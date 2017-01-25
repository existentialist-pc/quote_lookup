#!/usr/bin/env python3.5
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app


app = create_app()
manager = Manager(app)

if __name__ == '__main__':
    # db.create_all()
    manager.run()