import logging
from layer2table import GisLayer2Table


def main():
    
    log_format = '%(asctime)s|%(name)s|%(levelname)s|%(message)s'
    logging.basicConfig(filename='app.log', format=log_format,
                        encoding='utf-8', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info("Logger Created")

    urls = ["https://maps.cityofrochester.gov/server/rest/services/App_PropertyInformation/App_Tax_Parcel_Viewer/FeatureServer/0",
            "https://maps.cityofrochester.gov/server/rest/services/App_PropertyInformation/App_Tax_Parcel_Viewer/FeatureServer/011as"]

    output_path = "./scripts/generated"

    layer2table = GisLayer2Table(parent_logger=logger, conversion_table_source="data\EsriPostgresTypeConversion.json")
    
    for url in urls:
        result = layer2table.generateScript(url, output_type='tsql', output_path=output_path)
        print(result)
main()
