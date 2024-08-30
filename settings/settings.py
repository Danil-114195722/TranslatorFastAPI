import logging
from pathlib import Path


# полный путь до проекта
BASEDIR = Path(__file__).parent.parent

# настройка логирования
logger = logging.getLogger('fast-api-server')
logging.basicConfig(
    level=logging.INFO,
    filename=f'{BASEDIR}/logs/views_logs.log',
    format='%(levelname)s: (%(module)s, %(lineno)s) -- %(message)s',
)
