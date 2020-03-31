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
    description = 'Utah Lake Water Parameters'
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
                url='lake',
                controller='lake.controllers.home'
            ),
            UrlMap(
                name='add_data',
                url='lake/datas/add',
                controller='lake.controllers.add_data'
            ),
            UrlMap(
                name='instructions',
                url='lake/datas/instructions',
                controller='lake.controllers.instructions'
            ),
        )

        return url_maps
