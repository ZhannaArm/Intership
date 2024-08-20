from arango import ArangoClient
from constants import University


def main():
    client = ArangoClient(hosts="http://localhost:8529")
    sys_db = client.db('_system', username='root', password='openSesame')

    if not sys_db.has_database(University.UNIVERSITY):
        sys_db.create_database(University.UNIVERSITY)

    db = client.db(University.UNIVERSITY, username='root', password='openSesame')

    instructors_collection = db.create_collection(University.INSTRUCTORS)

    courses_collection = db.create_collection(University.COURSES)

    timeslots_collection = db.create_collection(University.TIME_SLOTS)


if __name__ == '__main__':
    main()
