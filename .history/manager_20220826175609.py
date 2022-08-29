# -*- coding: utf-8 -*-
from flask_script import Manager
from app import create_app, db
from config import config

app = create_app(config)

manager = Manager(app)

# migrate = Migrate(app, db)
# manager.add_command('db', MigrateCommand)


class StandaloneApplication(BaseApplication, ABC):
    """
    gunicorn服务器启动类
    """

    def __init__(self, application, options):
        self.application = application
        self.options = options or {}
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

@manager.command
def run():
    """
    生产模式启动命令函数
    To use: python3 manager.py run
    """
    app.logger.setLevel(app.config.get('LOG_LEVEL', logging.INFO))
    service_config = {
        'bind': app.config.get('BIND', '0.0.0.0:5000'),
        'workers': app.config.get('WORKERS', cpu_count() * 2 + 1),
        'worker_class': 'gevent',
        'worker_connections': app.config.get('WORKER_CONNECTIONS', 10000),
        'backlog': app.config.get('BACKLOG', 2048),
        'timeout': app.config.get('TIMEOUT', 60),
        'loglevel': app.config.get('LOG_LEVEL', 'info'),
        'pidfile': app.config.get('PID_FILE', 'run.pid'),
    }
    StandaloneApplication(app, service_config).run()

@manager.command
def debug():
    """
    debug模式启动命令函数
    To use: python3 manager.py debug
    """
    app.logger.setLevel(logging.DEBUG)

    # default port 5000
    app.run(host="0.0.0.0", debug=True)
    # app.run(debug=True)

if __name__ == '__main__':
    manager.run()
