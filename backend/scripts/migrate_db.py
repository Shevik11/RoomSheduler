import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

from models.models import Base

load_dotenv()

SQLALCHEMY_DATABASE_URL = f"postgresql://{os.getenv('NAME')}:{os.getenv('PASSWORD')}@{os.getenv('HOST')}/{os.getenv('DB_NAME')}"


def migrate_database():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    # create backup of data
    with engine.connect() as conn:
        # save data
        result = conn.execute(text("SELECT * FROM days_3"))
        data = result.fetchall()

        # drop old table
        conn.execute(text("DROP TABLE IF EXISTS days_3"))
        conn.commit()

        # create new table
        Base.metadata.create_all(bind=engine)

        # restore data
        if data:
            columns = result.keys()
            insert_stmt = text(
                f"""
                INSERT INTO days_3 ({', '.join(columns)})
                VALUES ({', '.join([':' + col for col in columns])})
            """
            )

            for row in data:
                conn.execute(insert_stmt, dict(zip(columns, row)))

            conn.commit()
            print("Migration completed successfully!")
        else:
            print("No data to migrate")


if __name__ == "__main__":
    migrate_database()
