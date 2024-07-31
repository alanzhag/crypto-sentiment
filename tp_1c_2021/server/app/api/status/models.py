import enum
from dataclasses import dataclass, field
from typing import List


class ServiceState(enum.Enum):
    UP = 1,
    DOWN = 2,

    def get_message(self, services=None):
        if self == self.UP:
            return "Todos los servicios operacionales"
        else:
            down_services = ": " + ','.join([s.name for s in services if s.status == ServiceState.DOWN]) \
                if services else ""
            return f"Algunos servicios no estan disponibles{down_services}"


@dataclass
class ServiceStatus:
    name: str
    status: ServiceState
    message: str = ""


@dataclass
class ApplicationStatus:
    status: ServiceState = field(init=False)
    message: str = field(init=False)
    detailed_message: str = field(init=False)
    services: List[ServiceStatus]

    def __post_init__(self):
        state = self._calculate_state(self.services)
        self.status = state
        self.message = state.get_message()
        self.detailed_message = state.get_message(self.services)

    @staticmethod
    def _calculate_state(services) -> ServiceState:
        return ServiceState.UP if all(
            [service.status == ServiceState.UP for service in services]) else ServiceState.DOWN