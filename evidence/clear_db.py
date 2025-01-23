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
        tag_ops.delete(engine, tag.name)

    groups = group_ops.get_all(engine)
    for group in groups:
        group_ops.delete(engine, group.name)

    people = person_ops.get_all(engine)
    for person in people:
        person_ops.delete(engine, person.name)
