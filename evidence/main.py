
from database.database_manager import DatabaseManager
from database.database_models import GroupType



def load_stuff(dbm: DatabaseManager):
    dbm.groups().create("elk lodge", GroupType.ORGANIZATION)
    dbm.groups().create("chess club", GroupType.ORGANIZATION)
    dbm.groups().create("The Gambino Family", GroupType.FAMILY)

    tag = dbm.tags().create("character")
    print(tag)

    dbm.people().create("spongebob", ["elk lodge", "chess club"])
    dbm.people().tag("spongebob", tag.name)
    dbm.people().add_affiliation("spongebob", "The Gambino Family")
    dbm.people().untag("spongebob", tag.name)

if __name__ == "__main__":
    dbm = DatabaseManager()
    load_stuff(dbm)


    groups = dbm.groups().get_all()
    for group in groups:
        print("Group:")
        print(group)
        print(group.members)
        print(group.tags)
        print("===")

    group = dbm.groups().get_by_id(1)

    print("Group (find by id)")
    print(group)
    print("===")

    group = dbm.groups().get_by_name("elk lodge")

    print("Group (find by name)")
    print(group)
    print("===")

