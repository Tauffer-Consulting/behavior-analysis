from ...models import Experiment, Group, Subject
import json


def populate_db_from_file(db, file_path):
    """Populate database with data from json file"""
    with open(str(file_path)) as json_file:
        data = json.load(json_file)
    populate_db(db=db, data=data)


def populate_db(db, data):
    """Populate database with a dictionary or json data (string)"""
    if isinstance(data, str):
        obj = json.loads(data)
    elif isinstance(data, dict):
        obj = data

    ne, ng, ns = 0, 0, 0
    for e in obj['Experiment']:
        ne += 1
        exp = Experiment(name=e['name'], description=e['description'])
        db.session.add(exp)

    for g in obj['Group']:
        ng += 1
        exp = Experiment.query.filter_by(name=g['experiment']).first()
        grp = Group(name=g['name'], experiment=exp)
        db.session.add(grp)

    for s in obj['Subject']:
        ns += 1
        grp = Group.query.filter_by(name=s['group']).first()
        sub = Subject(group=grp, file=s['file'])
        db.session.add(sub)

    db.session.commit()
    print(f"{ne} experiments, {ng} groups and {ns} subjects added to database")
