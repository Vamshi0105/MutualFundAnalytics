from sqlalchemy import create_engine

engine = create_engine(
    "sqlite:///bluestock_mf.db"
)

connection = engine.connect()

print("SQLite database created successfully.")

connection.close()