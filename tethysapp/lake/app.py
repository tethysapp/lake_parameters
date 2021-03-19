from tethys_sdk.base import TethysAppBase, url_map_maker


class Lake(TethysAppBase):
    """
    Tethys app class for Water Quality - Utah Lakes.
    """

    name = 'Water Quality - Utah Lakes'
    index = 'lake:data'
    icon = 'lake/images/lake.png'
    package = 'lake'
    root_url = 'lake'
    color = '#0c8fab'
    description = 'The Water Quality - Utah Lakes (WQ-UL) Web Application helps users understand what data are available in the AWQMS and BYU database, to provide easy access to the available data, to present the data in spatial (maps) and temporal (time series graphs) forms, and to help the users screen the data sources before export.'
    tags = '"Hydrology", "Utah Lakes", "Web Application", "Water Quality", "Tethys App"'
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='instructions',
                url='lake/instructions',
                controller='lake.controllers.instructions'
            ),
            UrlMap(
                name='data',
                url='lake/data',
                controller='lake.controllers.data'
            ),
            UrlMap(
                name='get_lake',
                url='lake/controllers/get_lake/',
                controller='lake.controllers.get_lake'
            ),
            UrlMap(
                name='param_fraction',
                url='lake/controllers/param_fraction/',
                controller='lake.controllers.param_fraction'
            ),
            UrlMap(
                name='lake_parameter',
                url='lake/controllers/lake_parameter/',
                controller='lake.controllers.lake_parameter'
            ),
            UrlMap(
                name='charact_data',
                url='lake/controllers/charact_data/',
                controller='lake.controllers.charact_data'
            ),
    )
        return url_maps
