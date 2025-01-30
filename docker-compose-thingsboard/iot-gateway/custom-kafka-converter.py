from thingsboard_gateway.connectors.converter import Converter
from thingsboard_gateway.tb_utility.tb_utility import log
from datetime import datetime
import pytz


class CustomKafkaUplinkConverter(Converter):
    def __init__(self, config):
        self.__config = config
        self.result_dict = {
            'deviceName': config.get('name', 'Cps-Device'),
            'deviceType': config.get('deviceType', 'default'),
            'attributes': [],
            'telemetry': {}
        }

    def convert(self, config, data):
        confkeys = ['attributes', 'telemetry']
        # Parsing the Struct data
        parsed_data = {}
        data.encode('utf-8')
        for entry in data.replace('Struct{', '').replace('}', '').split(','):
            key, value = entry.split('=', 1)
            parsed_data[key.strip()] = value.strip()

        for confkey in confkeys:
            self.result_dict[confkey] = []
            confkey_config = self.__config.get(confkey, [])
            confkey_data= {}
            message_valore = 0.0
            for field in confkey_config:
                key = field.get('key')
                if key in parsed_data:
                    value = parsed_data.get(key)
                    if field.get('type') == 'float':
                        value = self.convert_to_float(value)
                    if key == ('valore'):
                        message_valore = value
                    elif key == ('nome_parametro'):
                        confkey_data[value] = message_valore
                    elif key == ('data_registrazione'):
                        dt = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
                        dt = dt.replace(tzinfo=pytz.utc)
                        confkey_data['ts'] = int(dt.timestamp() * 1000)
                    else:
                        confkey_data[key] = value
            self.result_dict[confkey] = [confkey_data]

        log.info("Resulting dictionary: %s", self.result_dict)
        return self.result_dict

    def convert_to_float(self, value_str):
        try:
            return float(value_str)
        except ValueError:
            log.error("Float conversion failed for %s", value_str)
            return value_str  # return as string if conversion fails