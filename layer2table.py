import requests
import logging
import json
import os


class GisLayer2Table(object):
    def __init__(self, output_path, parent_logger=None, conversion_table_source=None):

        self.output_path = output_path
        # Supports logging. Pass a parent logger or one will be created
        if parent_logger:
            self._logger = parent_logger.getChild('gislayer2table')
        else:
            self._logger = logging.getLogger('gislayer2table')

        if conversion_table_source:
            self.conversion_table_source = conversion_table_source
        else:
            self._logger.error("No conversion table source provided")

        if not os.path.isdir(output_path):
            os.mkdir(output_path)

    def _getMetadata(self, feature_layer_url):
        try:
            response = requests.get(feature_layer_url + "/?f=json")
            if response.status_code != 200:
                raise Exception('{}: {} HTTP {}'.format(
                    response.request.url,
                    response.status_code,
                    response.text
                ))
            return response.json()

        except Exception as e:
            self._logger.error(e)

    def _getFields(self, metadata):
        fields = ''
        try:
            fields = metadata["fields"]
        except:
            self._logger.error(
                "Unable to find fields in dict, check your input object")
        return fields

    def _parseFields(self, field):
        result = dict(field_name=None, field_type=None)
        result['field_name'] = field['name']
        result['field_type'] = field['type']
        return result

    def _convertFields(self, field, conversion_dict):
        try:
            field['field_type'] = conversion_dict[field['field_type']]
            return field
        except:
            self._logger.debug(f"No field conversion found for {field}.")
            return f"Unable to convert {field}"
    def _writeScriptToFile(self, converted_fields):
       
        with open(self.output_path + "create_" + self.layer_name + ".sql", "w") as f:
                    f.write(f"CREATE TABLE {self.layer_name} (")
                    count = 0
                    for cf in converted_fields:
                        f.write(f"{cf['field_name']} {cf['field_type']}")
                        if count < len(converted_fields)-1:
                            f.write(',')
                        count = count + 1
                    f.write(");")
                    
    def generateScript(self, url):

        metadata = self._getMetadata(url)
        self.layer_name = metadata['name'].replace(' ', '')
        fields = self._getFields(metadata)
        if fields:
            parsed_fields = [self._parseFields(field) for field in fields]
            
            with open(self.conversion_table_source, 'r') as infile:
                conversion_dict = json.load(infile)
                
                converted_fields = [self._convertFields(
                    parsed_field, conversion_dict) for parsed_field in parsed_fields]
            # clean this up
            if converted_fields:
                self._writeScriptToFile(converted_fields)
