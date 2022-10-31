import logging
from layer2table import GisLayer2Table
from pprint import pprint


def main():
    # initialize and configure logger
    log_format = '%(asctime)s|%(name)s|%(levelname)s|%(message)s'
    logging.basicConfig(filename='app.log', format=log_format,
                        encoding='utf-8', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info("Logger Created")

    # set path for generated script output
    output_path = "generated-scripts/"

    g2t = GisLayer2Table(output_path=output_path, parent_logger=logger,
                         conversion_table_source="data\EsriPostgresTypeConversion.json")

    urls = ["https://maps.cityofrochester.gov/server/rest/services/App_PropertyInformation/App_Tax_Parcel_Viewer/FeatureServer/0",
            "https://maps.cityofrochester.gov/server/rest/services/App_PropertyInformation/App_Tax_Parcel_Viewer/FeatureServer/2",
            "https://maps.cityofrochester.gov/server/rest/services/App_PropertyInformation/App_Tax_Parcel_Viewer/FeatureServer/9",
            "https://maps.cityofrochester.gov/server/rest/services/App_PropertyInformation/App_Tax_Parcel_Viewer/FeatureServer/11"]

    for url in urls:
        result = g2t.generateScript(url)


main()
