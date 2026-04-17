"""
ETL entry point - loads hospital data from CSV files into Neo4j graph database.
"""
from src.hospital_bulk_csv_write import load_hospital_graph_from_csv

if __name__ == "__main__":
    load_hospital_graph_from_csv()
