import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

from .app import LiqInventory as app

Base = declarative_base()


# SQLAlchemy ORM definition for the dams table
class Site(Base):
    """
    SQLAlchemy Dam DB Model
    """
    __tablename__ = 'sites'

    # Columns
    id = Column(Integer, primary_key=True)
    lat = Column(Float)
    long = Column(Float)
    country = Column(String)
    city = Column(String)
    date_eq = Column(String)



def get_all_sites(db_directory):
    """
    Get all persisted dams.
    """
    # Write to file in {{db_directory}}/dams/{{uuid}}.json
    # Make dams dir if it doesn't exist
    sites_dir = os.path.join(db_directory, 'sites')
    if not os.path.exists(sites_dir):
        os.mkdir(sites_dir)

    sites = []

    # Open each file and convert contents to python objects
    for site_json in os.listdir(sites_dir):
        # Make sure we are only looking at json files
        if '.json' not in site_json:
            continue

        site_json_path = os.path.join(sites_dir, site_json)
        with open(site_json_path, 'r') as f:
            site_dict = json.loads(f.readlines()[0])
            sites.append(site_dict)

    return sites


def init_primary_db(engine, first_time):
    """
    Initializer for the primary database.
    """
    # Create all the tables
    Base.metadata.create_all(engine)

    # Add data
    if first_time:
        # Make session
        Session = sessionmaker(bind=engine)
        session = Session()

        # Initialize database with two dams
        site1 = Site(
            latitude=40.406624,
            longitude=-111.529133,
            country="Italy",
            city="L'Aquila",
            date_eq="2011"
        )

        site2 = Site(
            latitude=40.598168,
            longitude=-111.424055,
            country="United States",
            city="Valdez",
            date_eq="1964"
        )

        # Add the dams to the session, commit, and close
        session.add(site1)
        session.add(site2)
        session.commit()
        session.close()

import os
import uuid
import json


def add_new_site(db_directory, country, city, lat, long, date_eq):
    """
    Persist new dam.
    """
    # Serialize data to json
    new_site_id = uuid.uuid4()
    site_dict = {
        'id': str(new_site_id),
        'country': country,
        'city': city,
        'lat': lat,
        'long': long,
        'date_eq': date_eq
    }

    site_json = json.dumps(site_dict)

    # Write to file in {{db_directory}}/dams/{{uuid}}.json
    # Make dams dir if it doesn't exist
    sites_dir = os.path.join(db_directory, 'sites')
    if not os.path.exists(sites_dir):
        os.mkdir(sites_dir)

    # Name of the file is its id
    file_name = str(new_site_id) + '.json'
    file_path = os.path.join(sites_dir, file_name)

    # Write json
    with open(file_path, 'w') as f:
        f.write(site_json)
