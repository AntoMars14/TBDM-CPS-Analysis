from kafka import KafkaConsumer
import time
from threading import Thread
from thingsboard_gateway.connectors.connector import Connector
from thingsboard_gateway.tb_utility.tb_utility import log
from thingsboard_gateway.tb_utility.tb_loader import TBModuleLoader

class CustomKafkaConnector(Thread, Connector):
    def __init__(self, gateway, config, connector_type):
        super().__init__()
        self.statistics = {'MessagesReceived': 0, 'MessagesSent': 0}
        self.__config = config
        self.__gateway = gateway
        self.__connector_type = connector_type
        self.name = self.__config.get("name") or 'CustomKafkaConnector'
        log.info("Starting Custom %s connector", self.get_name())
        self.daemon = True
        self.stopped = True
        self.connected = False
        self.devices = {}
        self.consumer = None
        self.load_converters()
        self.__connect_to_kafka()
        log.info('Custom connector %s initialization success.', self.get_name())
        log.info("Devices in configuration file found: %s ", '\n'.join(device for device in self.devices))

    def __connect_to_kafka(self):
        try:
            self.consumer = KafkaConsumer(
                self.__config.get('topics', ['cps-machine-parameters']),
                bootstrap_servers=self.__config.get('bootstrap.servers', 'broker:29092'),
                value_deserializer=lambda m: m.decode('utf-8'),
                auto_offset_reset='earliest',
                enable_auto_commit=True
            )
            self.__gateway.add_device("Cps-Device", {"connector": self})
            self.connected = True
        except Exception as e:
            log.exception(e)
            self.connected = False

    def open(self):
        self.stopped = False
        self.start()

    def get_name(self):
        return self.name

    def is_connected(self):
        return self.connected

    def load_converters(self):
        devices_config = self.__config.get('devices')
        try:
            if devices_config is not None:
                for device_config in devices_config:
                    if device_config.get('converter') is not None:
                        converter =TBModuleLoader.import_module(self.__connector_type, device_config['converter'])
                        self.devices[device_config['name']] = {'converter': converter(device_config), 'device_config': device_config}
                    else:
                        log.error('Converter configuration for the custom connector %s -- not found, please check your configuration file.', self.get_name())
            else:
                log.error('Section "devices" in the configuration not found. A custom connector %s has being stopped.', self.get_name())
                self.close()
        except Exception as e:
            log.exception(e)

    def run(self):
        try:
            while not self.stopped:
                if not self.connected:
                    log.error("Not connected to Kafka. Retrying connection...")
                    time.sleep(5)  # Wait before retrying

                for message in self.consumer:
                    data_from_kafka = message.value
                    try:
                        for device in self.devices:
                            converted_data = self.devices[device]['converter'].convert(self.devices[device]['device_config'], data_from_kafka)
                            self.__gateway.send_to_storage(self.get_name(), self.get_id(), converted_data)
                            time.sleep(.1)
                    except Exception as e:
                        log.exception("Error processing data from Kafka: %s", e)
                        self.close()
                        raise e

                if not self.connected:
                    break
        except Exception as e:
            log.exception("Error in run method: %s", e)
        finally:
            if self.consumer is not None:
                self.consumer.close()

    def close(self):
        self.stopped = True
        if self.consumer is not None:
            try:
                log.info("Closing Kafka consumer...")
                self.consumer.close()
                self.connected = False
                log.info("Kafka consumer closed successfully.")
            except Exception as e:
                log.exception("Failed to close Kafka consumer: %s", e)
        else:
            log.warning("Kafka consumer is already None or closed.")

    def get_config(self):
        return self.__config

    def get_id(self):
        return self.__config.get('id', 'mycustomconnector1')

    def get_type(self):
        return self.__connector_type

    def is_stopped(self):
        return self.stopped

    def on_attributes_update(self, content):
        pass

    def server_side_rpc_handler(self, content):
        pass
