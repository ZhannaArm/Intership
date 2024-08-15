from arango import ArangoClient
from static_variables import University


def main():
    client = ArangoClient(hosts="http://localhost:8529")
    sys_db = client.db('_system', username='root', password='openSesame')

    if not sys_db.has_database(University.UNIVERSITY):
        sys_db.create_database(University.UNIVERSITY)

    db = client.db(University.UNIVERSITY, username='root', password='openSesame')

    if not db.has_collection(University.INSTRUCTORS):
        instructors_collection = db.create_collection(University.INSTRUCTORS)
    else:
        instructors_collection = db.collection(University.INSTRUCTORS)

    if not db.has_collection(University.COURSES):
        courses_collection = db.create_collection(University.COURSES)
    else:
        courses_collection = db.collection(University.COURSES)

    if not db.has_collection(University.TIME_SLOTS):
        timeslots_collection = db.create_collection(University.TIME_SLOTS)
    else:
        timeslots_collection = db.collection(University.TIME_SLOTS)


if __name__ == '__main__':
    main()
