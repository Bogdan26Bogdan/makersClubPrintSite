import unittest
from db import db
from datetime import datetime
from sqlalchemy import URL


IN_MEMORY_DB_URL = URL.create(
    drivername="sqlite+pysqlite",
    database="test_memory_db.db",
)


class TestDatabaseConnection(unittest.TestCase):
    def test_create_engine_instance(self):
        """Test that the database engine is created successfully."""
        engine = db.create_engine_instance(IN_MEMORY_DB_URL, echo=False)
        self.assertIsNotNone(engine)

    def test_insert_print(self):
        """Test inserting a PrintTracker record into the database."""
        engine = db.create_engine_instance(IN_MEMORY_DB_URL, echo=False)
        from db.print_tracker import PrintTracker
        from sqlalchemy.orm import Session

        new_print = PrintTracker(
            Name="Test User",
            PrintName="Test Print",
            GramsUsed=1500,
            Duration=120,
            Printer="Printer1",
            Color="Red",
            Completed=False,
            Submitted=datetime.now(),
        )

        with Session(engine) as session:
            session.add(new_print)
            session.commit()

            retrieved_print = (
                session.query(PrintTracker).filter_by(Name="Test User").first()
            )
            self.assertIsNotNone(retrieved_print)
            self.assertEqual(retrieved_print, new_print)

            session.commit()

    def test_insert_print_file(self):
        """Test inserting a PrintFile record into the database."""
        engine = db.create_engine_instance(IN_MEMORY_DB_URL, echo=False)
        from db.print_tracker import PrintTracker
        from db.print_file import PrintFile
        from sqlalchemy.orm import Session

        new_print = PrintTracker(
            Name="Test User",
            PrintName="Test Print",
            GramsUsed=1500,
            Duration=120,
            Printer="Printer1",
            Color="Red",
            Completed=False,
            Submitted=datetime.now(),
        )

        new_file = PrintFile(
            file_name="test_file.gcode",
            file_data=b"Sample G-code data",
            print_tracker_id=-1,  
        )

        with Session(engine) as session:
            session.add(new_print)
            session.commit()

            new_file.print_tracker_id = new_print.id
            session.add(new_file)
            session.commit()

            retrieved_file = (
                session.query(PrintFile).filter_by(print_tracker_id=new_print.id).first()
            )
            self.assertIsNotNone(retrieved_file)
            self.assertEqual(retrieved_file, new_file)
            
    def test_table_creation(self):
        """Test that the PrintTracker table is created in the database."""
        engine = db.create_engine_instance(IN_MEMORY_DB_URL, echo=False)
        
        from sqlalchemy import inspect
        from db.print_tracker import PrintTracker
        from db.print_file import PrintFile
        from db.user_and_role import User, Role

        inspector = inspect(engine)
        tables = inspector.get_table_names()

        self.assertIn(PrintTracker.__tablename__, tables)
        self.assertIn(PrintFile.__tablename__, tables)
        self.assertIn(User.__tablename__, tables)
        self.assertIn(Role.__tablename__, tables)
        self.assertIn('user_roles', tables)  # Association table
        self.assertEqual(len(tables), 5)

    def test_create_role_and_user(self):
        """Test creating a Role and User in the database."""
        engine = db.create_engine_instance(IN_MEMORY_DB_URL, echo=False)
        from db.user_and_role import User, Role
        from sqlalchemy.orm import Session

        new_role = Role(role="admin")
        new_user = User(email="testuser@example.com", password="hashed_password", date_created="2023-01-01", name="testuser")
        new_user.roles.append(new_role)

        with Session(engine, expire_on_commit=False) as session:
            session.add(new_role)
            session.add(new_user)
            session.commit()


        with Session(engine) as session:
            retrieved_user = session.query(User).filter_by(name="testuser").first()
            self.assertIsNotNone(retrieved_user)
            self.assertEqual(retrieved_user, new_user)
            self.assertIn(new_role, retrieved_user.roles)

            retrieved_role = session.query(Role).filter_by(role="admin").first()
            self.assertIsNotNone(retrieved_role)
            self.assertEqual(retrieved_role, new_role)
            self.assertIn(retrieved_role, new_user.roles)

            self.assertIn(retrieved_role, retrieved_user.roles)
            


if __name__ == "__main__":
    unittest.main()
