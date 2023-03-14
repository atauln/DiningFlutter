use TCDining;

drop table if exists ActiveDaysOfWeek;
drop table if exists Event;
drop table if exists Menu;
drop table if exists Location;

CREATE table Location (
	id INT PRIMARY KEY,
    name VARCHAR(64),
    summary VARCHAR(128),
    mapsUrl VARCHAR(64),
    department VARCHAR(32),
    mdoId INT,
    mapId INT,
    mrkId INT,
    catId INT
);

CREATE table Menu (
	id INT PRIMARY KEY,
    locationId INT,
    name VARCHAR(64),
    description VARCHAR(256),
    price DECIMAL(5, 2),
    category VARCHAR(64),
    eventId INT,
    foreign key (locationId) references Location(id)
);

CREATE table Event (
	id INT PRIMARY KEY,
    locationId INT,
    name VARCHAR(256),
    start DATETIME,
    end DATETIME,
    daysMask int,
    infinite boolean,
    foreign key (locationId) references Location (id)
);

CREATE table ActiveDaysOfWeek (
	id INT AUTO_INCREMENT PRIMARY KEY,
    eventId INT,
    sunday boolean,
    monday boolean,
    tuesday boolean,
    wednesday boolean,
    thursday boolean,
    friday boolean,
    saturday boolean,
    foreign key (eventId) references Event(id)
);

SHOW TABLES;