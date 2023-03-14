from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import Session

from datetime import datetime

import os

url = f"mysql://{os.environ['DB_USER']}:{os.environ['DB_PASS']}@{os.environ['DB_HOST']}/{os.environ['DB_USER']}"
engine = create_engine(url=url)


class Base(DeclarativeBase):
    pass

class Location(Base):
    __tablename__ = 'Location'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    summary = Column(String(128))
    mapsUrl = Column(String(64))
    department = Column(String(32))
    mdoId = Column(Integer)
    mapId = Column(Integer)
    mrktId = Column(Integer)
    catId = Column(Integer)

    def __repr__(self):
        return f"Location<{self.name}, {self.id}>"

class Menu(Base):
    __tablename__ = 'Menu'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    locationId = Column(Integer, ForeignKey('Location.id'), nullable=False)
    description = Column(String(256))
    price = Column(Float)
    category = Column(String(64))
    eventId = Column(Integer)

    def __repr__(self):
        return f"Menu<{self.name}, {self.id}, Location={self.locationId}>"

class Event(Base):
    __tablename__ = 'Event'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    locationId = Column(Integer, ForeignKey('Location.id'), nullable=False)
    start = Column(DateTime)
    end = Column(DateTime)
    daysMask = Column(Integer)
    infinite = Column(Boolean)

    def __repr__(self):
        return f"Event<{self.name}, {self.id}, Location={self.locationId}>"

class ActiveDaysOfWeek(Base):
    __tablename__ = 'ActiveDaysOfWeek'

    id = Column(Integer, primary_key=True)
    eventId = Column(Integer, ForeignKey('Event.id'), nullable=False)
    sunday = Column(Boolean)
    monday = Column(Boolean)
    tuesday = Column(Boolean)
    wednesday = Column(Boolean)
    thursday = Column(Boolean)
    friday = Column(Boolean)
    saturday = Column(Boolean)

    def __repr__(self):
        return f"ActiveDaysOfWeek<{self.eventId}, {self.day}>"

def setup_db(input: str) -> bool:
    if (len(input) == 0):
        return False
    
    locations = input.get("locations")

    for location in locations:
        with Session(engine) as session:
            proc_loc = Location(
                id=location.get("id"),
                name=location.get("name"),
                summary=location.get("summary"),
                mapsUrl=location.get("mapsUrl"),
                department=location.get("department"),
                mdoId=location.get("mdoId"),
                mapId=location.get("mapId"),
                mrktId=location.get("mrktId"),
                catId=location.get("catId")
            )

            session.add(proc_loc)

            for menu in location.get("menus"):
                proc_menu = Menu(
                    id=menu.get("id"),
                    name=menu.get("name"),
                    locationId=location.get("id"),
                    description=menu.get("description"),
                    price=menu.get("price"),
                    category=menu.get("category"),
                    eventId=menu.get("eventId")
                )

                session.add(proc_menu)
            
            for event in location.get("events"):
                proc_event = Event(
                    id=event.get("id"),
                    name=event.get("name"),
                    locationId=location.get("id"),
                    start=event.get("start"),
                    end=event.get("end"),
                    daysMask=event.get("daysMask"),
                    infinite=event.get("infinite")
                )sunday

                session.add(proc_event)

                for day in event.get("activeDaysOfWeek"):
                    proc_day = ActiveDaysOfWeek(
                        id=day.get("id"),
                        eventId=event.get("id"),
                        sunday=day.get("daysOfWeek").get("SUNDAY") != None,
                        monday=day.get("daysOfWeek").get("MONDAY") != None,
                        tuesday=day.get("daysOfWeek").get("TUESDAY") != None,
                        wednesday=day.get("daysOfWeek").get("WEDNESDAY") != None,
                        thursday=day.get("daysOfWeek").get("THURSDAY") != None,
                        friday=day.get("daysOfWeek").get("FRIDAY") != None,
                        saturday=day.get("daysOfWeek").get("SATURDAY") != None
                    )

                    session.add(proc_day)

            session.commit()

    return True


def empty_db():
    Base.metadata.drop_all(engine)
