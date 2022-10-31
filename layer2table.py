import json
import requests
import logging

class GisLayer2Table(object):
    def __init__(self, parent_logger=None) -> None:
        # Supports logging. Pass a parent logger or one will be created
        if parent_logger:
            self._logger = parent_logger.getChild('gislayer2table')
        else:
            self._logger = logging.getLogger('gislayer2table')
   
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
            self._logger.error("Unable to find fields in dict, check your input object")
        return fields
     
    def generateScript(self, url, output_path) -> None:
        print(output_path)
        metadata = self._get_metadata(url)
        fields = self._get_fields(metadata)
        
        
        

