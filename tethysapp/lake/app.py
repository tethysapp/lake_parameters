from tethys_sdk.base import TethysAppBase, url_map_maker


class Lake(TethysAppBase):
    """
    Tethys app class for Utah Lake Parameters.
    """

    name = 'Utah Lake Parameters'
    index = 'lake:home'
    icon = 'lake/images/lake.png'
    package = 'lake'
    root_url = 'lake'
    color = '#0c8fab'
    description = 'Utah Lake Water Parameters is an App that allows you to see the value distribution of a chosen parameter through the Utah Lake in the time'
    tags = '"Hydrology","CEEN 514", "Utah Lake"'
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='lake/home',
                controller='lake.controllers.home'
            ),
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
                name='interp',
                url='lake/interp',
                controller='lake.controllers.interp'
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
                name='charact_data',
                url='lake/controllers/charact_data/',
                controller='lake.controllers.charact_data'
            ),
    )
        return url_maps
