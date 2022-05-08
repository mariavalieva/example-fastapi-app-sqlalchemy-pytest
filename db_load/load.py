import json

from app import models
from app.db import SessionLocal, postgresql_engine

db = SessionLocal()
models.Base.metadata.create_all(postgresql_engine)

with open("db_load/data/teams.json", "r") as f:
    json_reader = json.load(f)

    for record in json_reader:
        db_record = models.Team(
            region=record["region"],
            noc=record["noc"],
        )
        db.add(db_record)
    db.commit()

with open("db_load/data/sport.json", "r") as f:
    json_reader = json.load(f)

    for record in json_reader:
        db_record = models.Sport(
            name=record["name"],
        )
        db.add(db_record)
    db.commit()

with open("db_load/data/events.json", "r") as f:
    json_reader = json.load(f)

    for record in json_reader:
        sport_id = (
            db.query(models.Sport).filter(
                models.Sport.name == record["sport"]
            ).first()
        )
        db_record = models.Event(name=record["event"], sport=sport_id)
        db.add(db_record)
    db.commit()

with open("db_load/data/games.json", "r") as f:
    json_reader = json.load(f)

    for record in json_reader:
        db_record = models.Game(
            year=int(record["year"]),
            season=record["season"],
            city=record["city"]
        )
        db.add(db_record)
    db.commit()

with open("db_load/data/athletes.json", "r") as f:
    json_reader = json.load(f)
    for record in list(json_reader):
        athlete_id = (
            db.query(models.Athlete)
            .filter(models.Athlete.name == record["name"])
            .first()
        )
        team_id = (
            db.query(models.Team).filter(
                models.Team.noc == record["team"]
            ).first()
        )
        height = int(record["height"]) if record["height"] != "NA" else None
        weight = float(record["weight"]) if record["weight"] != "NA" else None
        athlete_id = (
            db.query(models.Athlete)
            .filter(models.Athlete.name == record["name"])
            .first()
        )
        if athlete_id is None:
            db_record = models.Athlete(
                name=record["name"],
                team=team_id,
                sex=record["sex"],
                height=height,
                weight=weight,
            )
            db.add(db_record)
            db.commit()

with open("db_load/data/medals.json", "r") as f:
    json_reader = json.load(f)

    for record in json_reader:
        athlete_id = (
            db.query(models.Athlete)
            .filter(models.Athlete.name == record["athlete"])
            .first()
        )
        game_id = (
            db.query(models.Game)
            .filter(
                models.Game.season == record["games"].split()[1],
                models.Game.year == record["games"].split()[0],
            )
            .first()
        )
        event_id = (
            db.query(models.Event).filter(
                models.Event.name == record["event"]
            ).first()
        )
        if athlete_id:
            db_record = models.Medal(
                athlete=athlete_id,
                game=game_id,
                event=event_id,
                medal=record["type"],
            )
            db.add(db_record)
            db.commit()

db.close()
