import requests
import logging
import json
from pprint import pprint


class GisLayer2Table(object):
    def __init__(self, parent_logger=None, conversion_table_source=None) -> None:
        if parent_logger:
            self._logger = parent_logger.getChild('gislayer2table')
        else:
            self._logger = logging.getLogger('gislayer2table')
            
        if conversion_table_source:
            self.conversion_table_source = conversion_table_source
        else:
            self._logger.error("No conversion table source provided")
        # Supports logging. Pass a parent logger or one will be created
       

    def _get_metadata(self, feature_layer_url):
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

    def _get_fields(self, metadata):
        fields = ''
        try:
            fields = metadata["fields"]
        except:
            self._logger.error(
                "Unable to find fields in dict, check your input object")
        return fields

    def _parse_fields(self, field):
        result = dict(field_name=None, field_type=None)
        result['field_name'] = field['name']
        result['field_type'] = field['type']
        return result
        
    def _convertFields(self, field, output_type):
        
        with open(self.conversion_table_source, 'r') as infile:
            conversion_dict = json.load(infile)

        if output_type == 'tsql':
            try:
                field['field_type'] = conversion_dict[field['field_type']]
                return field
            except:
                self._logger.debug(f"No field conversion found for {field}.")
                return f"Unable to convert {field}"
        
    def generateScript(self, url, output_type, output_path) -> None:
        result = ''
        metadata = self._get_metadata(url)
        fields = self._get_fields(metadata)
        if fields:
            parsed_fields = [self._parse_fields(field) for field in fields]
            converted_fields = [self._convertFields(parsed_field, output_type) for parsed_field in parsed_fields]
        return result
    
        
