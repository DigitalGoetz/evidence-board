from database.database_manager import get_engine, load_some_people

if __name__ == "__main__":
    print("yarp")
    engine = get_engine()
    load_some_people(engine)