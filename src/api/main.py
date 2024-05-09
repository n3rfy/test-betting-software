from src.api import di
from src.api.application import create_application
from src.bets.infrastructure.database import DatabaseConfiguration


database_configuration = DatabaseConfiguration.from_env()
dependency_provider = di.DependencyProvider(
    database_configuration=database_configuration,
)
application = create_application(
    dependency_provider=dependency_provider,
)
