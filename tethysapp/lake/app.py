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
            UrlMap(
                name='show_data',
                url='lake/datas/show_data',
                controller='lake.controllers.show_data'
            ),
            UrlMap(
                name='chl_a',
                url='lake/datas/chl_a',
                controller='lake.controllers.chl_a'
            ),
            UrlMap(
                name='do',
                url='lake/datas/do',
                controller='lake.controllers.do'
            ),
            UrlMap(
                name='nit',
                url='lake/datas/nit',
                controller='lake.controllers.nit'
            ),
            UrlMap(
                name='ph',
                url='lake/datas/ph',
                controller='lake.controllers.ph'
            ),
            UrlMap(
                name='phosp',
                url='lake/datas/phosp',
                controller='lake.controllers.phosp'
            ),
            UrlMap(
                name='water_temp',
                url='lake/datas/water_temp',
                controller='lake.controllers.water_temp'
            ),
            UrlMap(
                name='tds',
                url='lake/datas/tds',
                controller='lake.controllers.tds'
            ),
            UrlMap(
                name='turb',
                url='lake/datas/turb',
                controller='lake.controllers.turb'
            ),
            UrlMap(
                name='secchi',
                url='lake/datas/secchi',
                controller='lake.controllers.secchi'
            ),
        )

        return url_maps
