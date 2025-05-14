#!/bin/bash
set -e

# Function to check if Neo4j is ready
check_neo4j() {
    echo "Checking Neo4j connection..."
    python -c "
import neo4j
import os
import time

def check_connection():
    uri = os.getenv('NEO4J_URI')
    user = os.getenv('NEO4J_USERNAME')
    password = os.getenv('NEO4J_PASSWORD')
    
    try:
        driver = neo4j.GraphDatabase.driver(uri, auth=(user, password))
        with driver.session() as session:
            result = session.run('RETURN 1')
            result.single()
        driver.close()
        return True
    except Exception as e:
        print(f'Neo4j connection failed: {e}')
        return False

# Try to connect for 5 minutes
for _ in range(30):
    if check_connection():
        print('Neo4j is ready!')
        exit(0)
    print('Waiting for Neo4j...')
    time.sleep(10)

print('Could not connect to Neo4j')
exit(1)
"
}

# Check if Neo4j is ready
check_neo4j

# Start the ETL process
echo "Starting ETL process..."
python -m src.main 