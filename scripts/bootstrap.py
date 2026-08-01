import asyncio
import sys
from pathlib import Path

# Add backend directory to sys.path so we can import app modules
backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.database.database import engine, Base, async_session_maker
from app.models.base import Admin, SystemSettings
from app.core.security import get_password_hash

async def init_db():
    print("Initializing SQLite database and tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully.")

async def seed_admin():
    async with async_session_maker() as session:
        print("Checking for existing admin user...")
        from sqlalchemy.future import select
        result = await session.execute(select(Admin).filter_by(email="admin@runtime.com"))
        admin = result.scalar_one_or_none()
        
        if not admin:
            print("Creating default admin user (admin@runtime.com / admin123)...")
            admin = Admin(
                email="admin@runtime.com",
                hashed_password=get_password_hash("admin123"),
                role="admin",
                is_active=True
            )
            session.add(admin)
            await session.commit()
            print("Admin user created.")
        else:
            print("Admin user already exists.")

async def seed_settings():
    default_settings = [
        {"key": "app_name", "value": "LeadRadar AI", "description": "Global application name"},
        {"key": "crawler_enabled", "value": "true", "description": "Whether the LinkedIn crawler is active"},
        {"key": "ai_enabled", "value": "true", "description": "Whether AI analysis is active"},
        {"key": "default_scheduler_interval", "value": "30", "description": "Scheduler interval in minutes"},
        {"key": "openai_model", "value": "gpt-4o", "description": "Default OpenAI model for analysis"},
        {"key": "linkedin_max_scroll", "value": "20", "description": "Max scrolls per page visit"}
    ]
    
    async with async_session_maker() as session:
        print("Seeding default system settings...")
        for setting in default_settings:
            from sqlalchemy.future import select
            result = await session.execute(select(SystemSettings).filter_by(key=setting["key"]))
            existing = result.scalar_one_or_none()
            if not existing:
                db_obj = SystemSettings(
                    key=setting["key"], 
                    value=setting["value"], 
                    description=setting["description"]
                )
                session.add(db_obj)
        await session.commit()
        print("System settings seeded.")

async def main():
    try:
        await init_db()
        await seed_admin()
        await seed_settings()
        print("Bootstrap complete! You can now run the server.")
    except Exception as e:
        print(f"Error during bootstrap: {e}")

if __name__ == "__main__":
    asyncio.run(main())
