from database.database_manager import get_engine
from database.database_operations import PersonOperations, GroupOperations
from database.database_models import GroupType

if __name__ == "__main__":
    print("yarp")
    engine = get_engine()
    person_ops = PersonOperations()
    group_ops = GroupOperations()
    
    group_ops.create(engine, "elk lodge", GroupType.ORGANIZATION)
    group_ops.create(engine, "chess club", GroupType.ORGANIZATION)
    
    person_ops.create(engine, "spongebob", ["elk lodge", "chess club"])
    
    group_ops.create(engine, "The Gambino Family", GroupType.FAMILY)
    
