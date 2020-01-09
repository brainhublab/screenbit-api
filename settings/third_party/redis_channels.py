sys.path.insert(0, os.path.abspath('..'))
from local_settings import REDIS_HOSTS

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": REDIS_HOSTS,
        },
    },
}
