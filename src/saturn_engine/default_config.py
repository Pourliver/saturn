import typing as t

import os

from .config import Env
from .config import RabbitMQConfig
from .config import RayConfig
from .config import SaturnConfig
from .config import ServicesManagerConfig
from .config import WorkerConfig
from .config import WorkerManagerConfig


class config(SaturnConfig):
    env = Env(os.environ.get("SATURN_ENV", "development"))
    worker_manager_url = os.environ.get(
        "SATURN_WORKER_MANAGER_URL", "http://localhost:5000"
    )

    class services_manager(ServicesManagerConfig):
        services = [
            "saturn_engine.worker.services.loggers.ConsoleLogging",
            "saturn_engine.worker.services.loggers.Logger",
            "saturn_engine.worker.services.metrics.MemoryMetrics",
            "saturn_engine.worker.services.rabbitmq.RabbitMQService",
        ]
        strict_services = True

    class worker(WorkerConfig):
        job_store_cls = "ApiJobStore"
        executor_cls = os.environ.get("SATURN_WORKER__EXECUTOR_CLS", "ProcessExecutor")

    class rabbitmq(RabbitMQConfig):
        url = os.environ.get("SATURN_AMQP_URL", "amqp://127.0.0.1/")

    class ray(RayConfig):
        local = os.environ.get("SATURN_RAY__LOCAL", "0") == "1"
        address = os.environ.get("SATURN_RAY__ADDRESS", "auto")
        enable_logging = True
        executor_actor_count = 4
        executor_actor_concurrency = 2
        executor_actor_cpu_count = 1.0

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
        static_definitions_jobs_selector: t.Optional[str] = os.environ.get(
            "SATURN_STATIC_DEFINITIONS_JOBS_SELECTOR"
        )
        work_items_per_worker = 10


class client_config(config):
    class services_manager(config.services_manager):
        services = [
            "saturn_engine.worker.services.rabbitmq.RabbitMQService",
        ]
