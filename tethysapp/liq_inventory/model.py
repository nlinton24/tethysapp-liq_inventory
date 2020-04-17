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

    # Relationships



def add_new_site(location, name, owner, river, date_built):
    """
    Persist new dam.
    """

    # Create new Dam record
    new_site = Site(
        latitude=lat,
        longitude=long,
        country=country,
        city=city,
        date_eq=date_eq
    )

    # Get connection/session to database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()

    # Add the new dam record to the session
    session.add(new_site)

    # Commit the session and close the connection
    session.commit()
    session.close()


def get_all_sites():
    """
    Get all persisted dams.
    """
    # Get connection/session to database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()

    # Query for all dam records
    sites = session.query(Site).all()
    session.close()

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
