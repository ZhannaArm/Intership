from arango import ArangoClient


def main():
    client = ArangoClient(hosts="http://localhost:8529")
    sys_db = client.db('_system', username='root', password='openSesame')

    if not sys_db.has_database('university_db'):
        sys_db.create_database('university_db')

    db = client.db('university_db', username='root', password='openSesame')

    if not db.has_collection('instructors'):
        instructors_collection = db.create_collection('instructors')
    else:
        instructors_collection = db.collection('instructors')

    if not db.has_collection('courses'):
        courses_collection = db.create_collection('courses')
    else:
        courses_collection = db.collection('courses')

    if not db.has_collection('timeslots'):
        timeslots_collection = db.create_collection('timeslots')
    else:
        timeslots_collection = db.collection('timeslots')


if __name__ == '__main__':
    main()
