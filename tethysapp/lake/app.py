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
                name='search_data',
                url='lake/datas/search',
                controller='lake.controllers.search_data'
            ),
            UrlMap(
                name='instructions',
                url='lake/datas/instructions',
                controller='lake.controllers.instructions'
            ),
            # UrlMap(
            #     name='select-lake',
            #     url='lake/base',
            #     controller='lake.controllers.base'
            # ),
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
                name='magn_total',
                url='lake/datas/magn_total',
                controller='lake.controllers.magn_total'
            ),
            UrlMap(
                name='magn_dis',
                url='lake/datas/magn_dis',
                controller='lake.controllers.magn_dis'
            ),
            UrlMap(
                name='nit_total',
                url='lake/datas/nit_total',
                controller='lake.controllers.nit_total'
            ),
            UrlMap(
                name='nit_dis',
                url='lake/datas/nit_dis',
                controller='lake.controllers.nit_dis'
            ),
            UrlMap(
                name='ph',
                url='lake/datas/ph',
                controller='lake.controllers.ph'
            ),
            UrlMap(
                name='phosp_total',
                url='lake/datas/phosp_total',
                controller='lake.controllers.phosp_total'
            ),
            UrlMap(
                name='phosp_dis',
                url='lake/datas/phosp_dis',
                controller='lake.controllers.phosp_dis'
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
            UrlMap(
                name='ortho',
                url='lake/datas/ortho',
                controller='lake.controllers.ortho'
            ),
    )

        return url_maps
