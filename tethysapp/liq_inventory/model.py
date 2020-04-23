import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

from .app import LiqInventory as app

Base = declarative_base()


class Site(Base):
    """
    SQLAlchemy Site DB Model
    """
    __tablename__ = 'sites'

    id = Column(Integer, primary_key=True)
    lat = Column(Float)
    long = Column(Float)
    country = Column(String)
    city = Column(String)
    date_eq = Column(String)



def get_all_sites(db_directory):
    """
    Get all persisted sites.
    """
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
    Base.metadata.create_all(engine)

    if first_time:
        Session = sessionmaker(bind=engine)
        session = Session()

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


    sites_dir = os.path.join(db_directory, 'sites')
    if not os.path.exists(sites_dir):
        os.mkdir(sites_dir)

    file_name = str(new_site_id) + '.json'
    file_path = os.path.join(sites_dir, file_name)


    with open(file_path, 'w') as f:
        f.write(site_json)
