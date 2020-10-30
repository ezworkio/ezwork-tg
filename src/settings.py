import os
from enum import Enum
from typing import Optional


class Envs(Enum):
    Development = 'development'
    Testing = 'testing'
    Stage = 'stage'
    Production = 'production'
    Uknown = 'unknown'

    @classmethod
    def from_string(cl, st: str) -> 'Envs':
        if st == 'development':
            return cl.Development
        elif st == 'testing':
            return cl.Testing
        elif st == 'stage':
            return cl.Stage
        elif st == 'production':
            return cl.Production
        else:
            return cl.Uknown


_env = Envs.from_string(os.environ['ENV_CONFIG'])


class PgConfig:
    def __init__(self,
                 user=None,
                 password=None,
                 database=None,
                 host='localhost',
                 port=5432):

        if not all((user, password, database, host, port)):
            raise ValueError("All parameters should not been None")

        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.port = port

    @property
    def uri(self):
        """Returns database URI"""
        return (f'postgresql://{self.user}:{self.password}@'
                f'{self.host}:{self.port}/{self.database}')


class PgConfigMixin:
    def init_database(self):
        self.PGPARAMS = PgConfig(
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            database=os.environ['DB_NAME'],
            host=os.environ['DB_HOST'],
            port=os.environ['DB_PORT']
        )


class RabbitMQConfig:
    def __init__(self, user, password, virtual_host, host, port):

        if not all((user, password, virtual_host, host, port)):
            raise ValueError("All parameters should not been None")

        self.user = user
        self.password = password
        self.virtual_host = virtual_host
        self.host = host
        self.port = port


class RabbitConfigMixin:
    def init_rabbitmq(self):
        self.RMQPARAMS = RabbitMQConfig(
            user=os.environ.get('RABBITMQ_USER', 'guest'),
            password=os.environ.get('RABBITMQ_PASSWORD', 'guest'),
            virtual_host=os.environ.get('RABBITMQ_VIRTUAL_HOST', '/'),
            host=os.environ.get('RABBITMQ_HOST', 'localhost'),
            port=os.environ.get('RABBITMQ_PORT', 5672)
        )


class DevelopmentConfig(PgConfigMixin, RabbitConfigMixin):

    def __init__(self):  # pragma: no cover
        self.init_database()
        self.init_rabbitmq()

        self.DEBUG = True


class StageConfig(PgConfigMixin, RabbitConfigMixin):

    def __init__(self):  # pragma: no cover
        self.init_database()
        self.init_rabbitmq()

        self.DEBUG = False


class TestingConfig(PgConfigMixin):
    def __init__(self):  # pragma: no cover
        self.init_database()

        self.DEBUG = True
        self.TESTING = True


def load_config(env: Optional[Envs]=None):
    """Create config based on environment.
    Written as a function for easily mock if needed"""
    env = env or _env

    if env == Envs.Development:
        config = DevelopmentConfig()

    # stubs for future if poc succeeds
    elif env == Envs.Stage:
        config = StageConfig()

    elif env == Envs.Testing:
        config = TestingConfig()

    else:
        raise Exception(f"Don't know how to initialize config "
                        f"in '{env}' environment")

    config.SQLALCHEMY_DATABASE_URI = config.PGPARAMS.uri
    config.SQLALCHEMY_TRACK_MODIFICATIONS = False

    return config
