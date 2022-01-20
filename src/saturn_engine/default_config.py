import os

from .config import Env
from .config import RabbitMQConfig
from .config import RayConfig
from .config import SaturnConfig
from .config import WorkerConfig
from .config import WorkerManagerConfig


class config(SaturnConfig):
    env = Env(os.environ.get("SATURN_ENV", "development"))

    class worker(WorkerConfig):
        job_store_cls = "ApiJobStore"
        executor_cls = os.environ.get("SATURN_WORKER__EXECUTOR_CLS", "ProcessExecutor")
        worker_manager_url = os.environ.get(
            "SATURN_WORKER_MANAGER_URL", "http://localhost:5000"
        )
        services = [
            "saturn_engine.worker.services.loggers.ConsoleLogging",
            "saturn_engine.worker.services.loggers.Logger",
            "saturn_engine.worker.services.metrics.MemoryMetrics",
            "saturn_engine.worker.services.rabbitmq.RabbitMQService",
        ]
        strict_services = True

    class rabbitmq(RabbitMQConfig):
        url = os.environ.get("SATURN_AMQP_URL", "amqp://127.0.0.1/")

    class ray(RayConfig):
        local = os.environ.get("SATURN_RAY__LOCAL", "0") == "1"
        address = os.environ.get("SATURN_RAY__ADDRESS", "auto")

    class worker_manager(WorkerManagerConfig):
        flask_host = os.environ.get("SATURN_FLASK_HOST", "127.0.0.1")
        flask_port = int(os.environ.get("SATURN_FLASK_PORT", 5000))
        database_url: str = os.environ.get("SATURN_DATABASE_URL", "sqlite:///test.db")
        async_database_url: str = (
            os.environ.get("SATURN_DATABASE_URL", "sqlite:///test.db")
            .replace("sqlite:/", "sqlite+aiosqlite:/")
            .replace("postgresql:/", "postgresql+asyncpg:/")
        )
        static_definitions_directory: str = os.environ.get(
            "SATURN_STATIC_DEFINITIONS_DIR", "/opt/saturn/definitions"
        )
