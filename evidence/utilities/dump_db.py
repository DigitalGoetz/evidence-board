from database.database_manager import get_engine
from database.database_operations import (
    PersonOperations,
    GroupOperations,
    TagOperations,
)

if __name__ == "__main__":

    engine = get_engine()
    person_ops = PersonOperations()
    group_ops = GroupOperations()
    tag_ops = TagOperations()

    tags = tag_ops.get_all(engine)
    for tag in tags:
        print(tag)

    groups = group_ops.get_all(engine)
    for group in groups:
        print(group)

    people = person_ops.get_all(engine)
    for person in people:
        print(person)
