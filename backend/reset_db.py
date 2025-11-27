"""
Reset database - Drop all tables and recreate them
"""
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine, SessionLocal
from sqlalchemy import text

def reset_database():
    """Drop all tables and recreate them"""
    print("🗑️  Resetting database...")
    
    db = SessionLocal()
    
    try:
        # Drop all tables with CASCADE to remove all dependencies
        print("Dropping all tables with CASCADE...")
        
        # Get all table names
        result = db.execute(text("""
            SELECT tablename FROM pg_tables 
            WHERE schemaname = 'public'
        """))
        tables = [row[0] for row in result]
        
        # Drop each table with CASCADE
        for table in tables:
            print(f"  Dropping table: {table}")
            db.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
        
        db.commit()
        print("✅ All tables dropped")
        
        # Also drop all sequences
        print("\nDropping all sequences...")
        result = db.execute(text("""
            SELECT sequence_name FROM information_schema.sequences 
            WHERE sequence_schema = 'public'
        """))
        sequences = [row[0] for row in result]
        
        for sequence in sequences:
            print(f"  Dropping sequence: {sequence}")
            db.execute(text(f"DROP SEQUENCE IF EXISTS {sequence} CASCADE"))
        
        db.commit()
        print("✅ All sequences dropped")
        
        print("\n✅ Database reset successfully!")
        print("\n📝 Next step: Run 'pipenv run python init_db.py' to populate with initial data")
        
    except Exception as e:
        print(f"\n❌ Error resetting database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    confirm = input("⚠️  This will DELETE ALL DATA. Are you sure? (yes/no): ")
    if confirm.lower() == "yes":
        reset_database()
    else:
        print("❌ Reset cancelled")

