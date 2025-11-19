from app.core.crud_base import CRUDBase
from app.models.maintenance.asset_failure_mode_model import (
    MaintenanceFailureSymptom, 
    MaintenanceFailureMode, 
    MaintenanceFailureCause
)
from .failure_analysis_schemas import RCAItemCreate, RCAItemUpdate

# Criamos instâncias CRUD genéricas para cada entidade
crud_symptom = CRUDBase[MaintenanceFailureSymptom, RCAItemCreate, RCAItemUpdate](MaintenanceFailureSymptom)
crud_mode = CRUDBase[MaintenanceFailureMode, RCAItemCreate, RCAItemUpdate](MaintenanceFailureMode)
crud_cause = CRUDBase[MaintenanceFailureCause, RCAItemCreate, RCAItemUpdate](MaintenanceFailureCause)