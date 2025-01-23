from database.database_manager import get_engine
from database.database_operations import PersonOperations, GroupOperations, TagOperations
from database.database_models import GroupType

if __name__ == "__main__":
    engine = get_engine()
    person_ops = PersonOperations()
    group_ops = GroupOperations()
    tag_ops = TagOperations()
    
    group_ops.create(engine, "elk lodge", GroupType.ORGANIZATION)
    group_ops.create(engine, "chess club", GroupType.ORGANIZATION)
    
    person_ops.create(engine, "spongebob", ["elk lodge", "chess club"])
    
    group_ops.create(engine, "The Gambino Family", GroupType.FAMILY)

    person_ops.add_affiliation(engine, "spongebob", "The Gambino Family")

    tag = tag_ops.create(engine, "character")

    person_ops.untag(engine, "spongebob", "character")

    
    
