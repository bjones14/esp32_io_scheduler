'''
Helper functions used by various parts of the application.

'''
def load_config(file_path: str = 'config.json') -> config:
  """
  This method will load the JSON configuration file and create all of the scheduler objects
  that are requested in the configuration.  This method will prepare the scheduler to be run
  but will not command it to run.  It will return a key-value dictionary of the configuration
  items.

  Args:
      file_path (str, optional): Location of the JSON config file. Defaults to 'config.json'.

  Returns:
      cfg: A config object that contains all of the loaded configuration.
  """
  with open(file_path) as file: 
    json_dict = json.loads(file)
    cfg = config(json_dict)

  return cfg


def mqtt_subscribe_cb(topic: str, msg: str):
  """
  Callback method that is executed anytime an MQTT message is received.

  Args:
      topic (str): The MQTT topic that was received
      msg (str): The MQTT message that was received
  """
  print((topic, msg))
  if topic == b'notification' and msg == b'received':
    print('ESP received hello message')


def mqtt_connect_and_subscribe(cfg: config):

  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()