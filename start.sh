docker run -d \
  --name myps \
  -e rabbitmq_host=xxxx \
  -e rabbitmq_port=5672 \
  -e rabbitmq_username=xxxx \
  -e rabbitmq_password=xxxx \
  -e rabbitmq_queue_name=portscan \
  -e mongo_host=xxxx \
  -e mongo_port=27017 \
  -e mongo_username=xxxxx \
  -e mongo_password=xxxxx \
  -e mongo_database=src \
  --restart always \
  smilexxfire/portscan
