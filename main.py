from typing import Union, Any

import requests
import urllib.parse


class IncapsulaGen():
    def __init__(self, session: requests.Session, script: str, user_data: dict[str, Any]) -> None:
        self._session: requests.Session = requests.Session()
        self.script: str = script

        self.create_data()
        
    def create_data(self) -> str:
        data: list[tuple[str, str]] = [
            ('navigator', 'exists'),
            ('navigator.vendor', 'value'),
            ('navigator.appName', 'value'),
            ('navigator.plugins.length==0', 'value'),
            ('navigator.platform', 'value'),
            ('navigator.webdriver', 'value'),
            ('platform', 'plugin_extentions'),
            ('ActiveXObject', 'exists'),
            ('webkitURL', 'exists'),
            ('_phantom', 'exists'),
            ('callPhantom', 'exists'),
            ('chrome', 'exists'),
            ('yandex', 'exists'),
            ('opera', 'exists'),
            ('opr', 'exists'),
            ('safari', 'exists'),
            ('awesomium', 'exists'),
            ('puffinDevice', 'exists'),
            ('__nightmare', 'exists'),
            ('domAutomation', 'exists'),
            ('domAutomationController', 'exists'),
            ('_Selenium_IDE_Recorder', 'exists'),
            ('document.__webdriver_script_fn', 'exists'),
            ('document.$cdc_asdjflasutopfhvcZLmcfl_', 'exists'),
            ('process.version', 'exists'),
            ('global.require', 'exists'),
            ('global.process', 'exists'),
            ('WebAssembly', 'exists'),
            ("require('fs')", 'exists'),
            ('globalThis==global', 'value'),
            ('window.toString()', 'value'),
            ('navigator.cpuClass', 'exists'),
            ('navigator.oscpu', 'exists'),
            ('navigator.connection', 'exists'),
            ("navigator.language=='C'", 'value'),
            ('Object.keys(window).length', 'value'),
            ('window.outerWidth==0', 'value'),
            ('window.outerHeight==0', 'value'),
            ('window.WebGLRenderingContext', 'exists'),
            ('window.constructor.toString()', 'value'),
            ("Boolean(typeof process !== 'undefined' && process.versions && process.versions.node)", 'value'),
            ('document.documentMode', 'value'),
            ('eval.toString().length', 'value'),
            ('navigator.connection.rtt', 'value'),
            ('deviceType', 'function'),
            ('screen.width', 'value'),
            ('screen.height', 'value'),
            ('eoapi', 'exists'),
            ('eoapi_VerifyThis', 'exists'),
            ('eoapi_extInvoke', 'exists'),
            ('eoWebBrowserDispatcher', 'exists'),
            ('window.HIDDEN_CLASS', 'exists'),
            ('navigator.mimeTypes.length==2', 'value'),
            ('navigator.plugins.length==2', 'value'),
            ('window.globalThis', 'exists'),
            ('navigator.userAgentData.brands[0].brand', 'value'),
            ('navigator.userAgentData.brands[1].brand', 'value'),
            ('navigator.userAgentData.brands[2].brand', 'value'),
            ("navigator.plugins('Microsoft Edge PDF Plugin')", 'exists')
        ]
        
        formattedData: str = urllib.parse.quote(
            ''.join(['='.join(tups) for tups in data])
        )

        return formattedData
       
       
       
if __name__ == '__main__':
    IncapsulaGen(
        requests.Session(),
        '',
        {
            'userAgent': 'test'
        }
    )