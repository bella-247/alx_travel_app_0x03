import pymysql
pymysql.install_as_MySQLdb()

# ensure Celery app is loaded when django starts
from .celery import app as celery_app


__all__ = ("celery_app",)