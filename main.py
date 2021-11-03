from typing import Union, Any

import requests
import urllib.parse


class IncapsulaGen():
    def __init__(self, session: requests.Session, script: str, user_data: dict[str, Any]) -> None:
        self._session: requests.Session = requests.Session()
        self.script: str = script
        self.user_data: dict[str, str] = user_data

        self.create_data()
    
    def create_data(self) -> str:
        """Formats all the data into a list[tuple] and encodes it to the needed format."""
        
        # There probably is a better way to do this but I did it like this to keep it easy if you want to use your own collector/add fields
        data: list[tuple[str, str]] = [
            ('navigator', self.user_data['navigator']),
            ('navigator.vendor', self.user_data['navigator.vendor']),
            ('navigator.appName', self.user_data['navigator.appName']),
            ('navigator.plugins.length==0', self.user_data['navigator.plugins.length==0']),
            ('navigator.platform', self.user_data['navigator.platform']),
            ('navigator.webdriver', self.user_data['navigator.webdriver']),
            # ('platform', self.user_data['platform']), # Field gets collected but never actually used
            ('ActiveXObject', self.user_data['ActiveXObject']),
            ('webkitURL', self.user_data['webkitURL']),
            ('_phantom', self.user_data['_phantom']),
            ('callPhantom', self.user_data['callPhantom']),
            ('chrome', self.user_data['chrome']),
            ('yandex', self.user_data['yandex']),
            ('opera', self.user_data['opera']),
            ('opr', self.user_data['opr']),
            ('safari', self.user_data['safari']),
            ('awesomium', self.user_data['awesomium']),
            ('puffinDevice', self.user_data['puffinDevice']),
            ('__nightmare', self.user_data['__nightmare']),
            ('domAutomation', self.user_data['domAutomation']),
            ('domAutomationController', self.user_data['domAutomationController']),
            ('_Selenium_IDE_Recorder', self.user_data['_Selenium_IDE_Recorder']),
            ('document.__webdriver_script_fn', self.user_data['document.__webdriver_script_fn']),
            ('document.$cdc_asdjflasutopfhvcZLmcfl_', self.user_data['document.$cdc_asdjflasutopfhvcZLmcfl_']),
            ('process.version', self.user_data['process.version']),
            ('global.require', self.user_data['global.require']),
            ('global.process', self.user_data['global.process']),
            ('WebAssembly', self.user_data['WebAssembly']),
            ("require('fs')", self.user_data["require('fs')"]),
            ('globalThis==global', self.user_data['globalThis==global']),
            ('window.toString()', self.user_data['window.toString()']),
            ('navigator.cpuClass', self.user_data['navigator.cpuClass']),
            ('navigator.oscpu', self.user_data['navigator.oscpu']),
            ('navigator.connection', self.user_data['navigator.connection']),
            ("navigator.language=='C'", self.user_data["navigator.language=='C'"]),
            ('Object.keys(window).length', self.user_data['Object.keys(window).length']),
            ('window.outerWidth==0', self.user_data['window.outerWidth==0']),
            ('window.outerHeight==0', self.user_data['window.outerHeight==0']),
            ('window.WebGLRenderingContext', self.user_data['window.WebGLRenderingContext']),
            ('window.constructor.toString()', self.user_data['window.constructor.toString()']),
            ("Boolean(typeof process !== 'undefined' && process.versions && process.versions.node)", self.user_data["Boolean(typeof process !== 'undefined' && process.versions && process.versions.node)"]),
            ('document.documentMode', self.user_data['document.documentMode']),
            ('eval.toString().length', self.user_data['eval.toString().length']),
            ('navigator.connection.rtt', self.user_data['navigator.connection.rtt']),
            ('deviceType', self.user_data['deviceType']),
            ('screen.width', self.user_data['screen.width']),
            ('screen.height', self.user_data['screen.height']),
            ('eoapi', self.user_data['eoapi']),
            ('eoapi_VerifyThis', self.user_data['eoapi_VerifyThis']),
            ('eoapi_extInvoke', self.user_data['eoapi_extInvoke']),
            ('eoWebBrowserDispatcher', self.user_data['eoWebBrowserDispatcher']),
            ('window.HIDDEN_CLASS', self.user_data['window.HIDDEN_CLASS']),
            ('navigator.mimeTypes.length==2', self.user_data['navigator.mimeTypes.length==2']),
            ('navigator.plugins.length==2', self.user_data['navigator.plugins.length==2']),
            ('window.globalThis', self.user_data['window.globalThis']),
            ('navigator.userAgentData.brands[0].brand', self.user_data['navigator.userAgentData.brands[0].brand']),
            ('navigator.userAgentData.brands[1].brand', self.user_data['navigator.userAgentData.brands[1].brand']),
            ('navigator.userAgentData.brands[2].brand', self.user_data['navigator.userAgentData.brands[2].brand']),
            ("navigator.plugins('Microsoft Edge PDF Plugin')", self.user_data["navigator.plugins['Microsoft Edge PDF Plugin']"])
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
            'navigator': 'true',
            'navigator.vendor': 'Google Inc.',
            'navigator.appName': 'Netscape',
            'navigator.plugins.length==0': 'false',
            'navigator.platform': 'Win32',
            'navigator.webdriver': 'false',
            'plugin_ext': 'no extention',
            'ActiveXObject': 'false',
            'webkitURL': 'true',
            '_phantom': 'false',
            'callPhantom': 'false',
            'chrome': 'true',
            'yandex': 'false',
            'opera': 'false',
            'opr': 'false',
            'safari': 'false',
            'awesomium': 'false',
            'puffinDevice': 'false',
            '__nightmare': 'false',
            'domAutomation': 'false',
            'domAutomationController': 'false',
            '_Selenium_IDE_Recorder': 'false',
            'document.__webdriver_script_fn': 'false',
            'document.$cdc_asdjflasutopfhvcZLmcfl_': 'false',
            'process.version': 'false',
            'global.require': 'false',
            'global.process': 'false',
            'WebAssembly': 'true',
            "require('fs')": 'false',
            'globalThis==global': 'cannot evaluate',
            'window.toString()': '[object Window]',
            'navigator.cpuClass': 'false',
            'navigator.oscpu': 'false',
            'navigator.connection': 'true',
            "navigator.language=='C'": 'false',
            'Object.keys(window).length': '212',
            'window.outerWidth==0': 'false',
            'window.outerHeight==0': 'false',
            'window.WebGLRenderingContext': 'true',
            'window.constructor.toString()': 'function Window() { [native code] }',
            "Boolean(typeof process !== 'undefined' && process.versions && process.versions.node)": 'false',
            'document.documentMode': 'undefined',
            'eval.toString().length': '33',
            'navigator.connection.rtt': '50',
            'deviceType': 'desktop',
            'screen.width': '2560',
            'screen.height': '1440',
            'eoapi': 'false',
            'eoapi_VerifyThis': 'false',
            'eoapi_extInvoke': 'false',
            'eoWebBrowserDispatcher': 'false',
            'window.HIDDEN_CLASS': 'false',
            'navigator.mimeTypes.length==2': 'true',
            'navigator.plugins.length==2': 'false',
            'window.globalThis': 'true',
            'navigator.userAgentData.brands[0].brand': 'Google Chrome',
            'navigator.userAgentData.brands[1].brand': 'Chromium',
            'navigator.userAgentData.brands[2].brand': ';Not A Brand',
            "navigator.plugins['Microsoft Edge PDF Plugin']": 'false'
        }
    )