from ..local_settings import REDIS_HOSTS

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": REDIS_HOSTS,
        },
    },
}
