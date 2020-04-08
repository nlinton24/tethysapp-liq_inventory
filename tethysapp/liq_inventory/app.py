from tethys_sdk.base import TethysAppBase, url_map_maker


class LiqInventory(TethysAppBase):
    """
    Tethys app class for Gravel Liquefaction Inventory.
    """

    name = 'Gravel Liquefaction Inventory'
    index = 'liq_inventory:home'
    icon = 'liq_inventory/images/logo.jpg'
    package = 'liq_inventory'
    root_url = 'liq-inventory'
    color = '#000000'
    description = 'An Inventory of Gravel Liquefaction Sites'
    tags = ''
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
                url='liq_inventory',
                controller='liq_inventory.controllers.home'
            ),
            UrlMap(
                name='help',
                url='help',
                controller='liq_inventory.controllers.help'
            ),
            UrlMap(
                name='about',
                url='about',
                controller='liq_inventory.controllers.about'
            )
        )

        return url_maps
