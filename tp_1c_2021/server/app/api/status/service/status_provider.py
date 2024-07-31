from app import db
from app.api.status.models import ServiceState, ServiceStatus
from app.persistence.services.firebase_persistence import firebase_persistence_service


def db_status():
    name = db.engine.name
    message = ""
    try:
        db.session.execute('SELECT 1')
        status = ServiceState.UP
    except Exception as e:
        message = str(e)
        status = ServiceState.DOWN
    return ServiceStatus(name=name, status=status, message=message)


def firebase_status():
    name = "firestore"
    try:
        firebase_persistence_service.get_last_n("test")
        return ServiceStatus(name=name, status=ServiceState.UP)
    except Exception as e:
        return ServiceStatus(name=name, status=ServiceState.DOWN, message=str(e))


class StatusProvider:
    @staticmethod
    def services_status():
        return [db_status(), firebase_status()]
