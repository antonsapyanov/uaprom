from config import redis_config
from app import PubSubApplication


app = PubSubApplication(redis_config['REDIS_HOST'], redis_config['REDIS_PORT'])
app.run()
