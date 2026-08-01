from app.database.database import Base

# Import all models here so Alembic can discover them
from app.models.admin import Admin
from app.models.system_settings import SystemSettings
from app.models.keyword import Keyword
from app.models.job_execution import JobExecution
from app.models.lead import Lead
