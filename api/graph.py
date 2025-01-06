from neo4j import GraphDatabase
import os
import uuid

# MATCH (n) RETURN n;

class GraphClient:

    def __init__(self):
        new4j_uri = os.environ.get('NEO4J_URI', "bolt://localhost:7687")
        username = os.environ.get('NEO4J_USERNAME', "neo4j")
        password = os.environ.get('NEO4J_PASSWORD', "password")
        self.driver = GraphDatabase.driver(new4j_uri, auth=(username, password))
    
    # Function to create a node
    def _create_node(self, label, properties):
        with self.driver.session() as session:
            session.execute_write(self._add_node, label, properties)

    # Transaction function to create a node
    def _add_node(self, tx, label, properties):
        query = f"CREATE (n:{label} $props)"
        print(f"Performing: {query}")
        tx.run(query, props=properties)

    def create_entry(self, title: str, description: str):
        self._create_node("Person", {"name": title, "description": description, "uuid": uuid.uuid4()})

    def get_entries(self):
        with self.driver.session() as session:
            result = session.run("MATCH (n) RETURN n, id(n) as nodeId")
            print(result)
            nodes = [dict(record["n"]) for record in result]
            return nodes
