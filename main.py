from typing import Union, Any

import requests
import urllib.parse
import base64

from deobfuscator import Incapsula_Deobfuscator

class IncapsulaGen():
    def __init__(self, session: requests.Session, user_data: dict[str, Any], debug: bool = False) -> None:
        self._session: requests.Session = session
        self._user_data: dict[str, str] = user_data
        self._debug: bool = debug
        
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self._user_data['navigator.userAgent'],
        }
        
    def print_message(self, message: str) -> None:
        if self._debug:
            print(f'[INCAPSULA SOLVER] {message}')
            
    def solve_challenge(self, challenge_script_url: str) -> str:
        """ Function that will actually solve the challenge, main function """
        
        self.print_message(f'Solving challenge: {challenge_script_url}')
        
        deobfuscator_instance: Incapsula_Deobfuscator = Incapsula_Deobfuscator(debug=self._debug)
        
        script = self.get_challenge_script(challenge_script_url)
        deobfuscated_script: str = deobfuscator_instance.deob_script(script)
        self.print_message('Deobfuscated script.')
            
        cookie_secret_key: str = self.find_cookie_key(deobfuscated_script)
        
        return self.create_cookie(
            cookie_secret_key
        )
    
    def get_challenge_script(self, challenge_script_url: str) -> str:            
        try:
            r = self._session.get(challenge_script_url, headers=self.headers)
        except Exception:
            raise Exception('Failed to fetch challenge script.')
        else:   
            return r.text
        
    def find_cookie_key(self, script: str) -> str:
        self.print_message('Finding cookie secret key.')
        
        secret_key_var_name: str = list(reversed(script.split("['substr'](0x0,0x5))+'digest='")[0].split(',')))[0]
        secret_key: str = (script.split(f"{secret_key_var_name}='")[1].split("'")[0])
        
        self.print_message(f'Found secret cookie key: {secret_key}')
        return secret_key
    
    def create_data(self) -> str:
        """Formats all the data into a list[tuple] and encodes it to the needed format."""
        
        # There probably is a better way to do this but I did it like this to keep it easy if you want to use your own collector/add fields
        data: list[tuple[str, str]] = [
            ('navigator', self._user_data['navigator']),
            ('navigator.vendor', self._user_data['navigator.vendor']),
            ('navigator.appName', self._user_data['navigator.appName']),
            ('navigator.plugins.length==0', self._user_data['navigator.plugins.length==0']),
            ('navigator.platform', self._user_data['navigator.platform']),
            ('navigator.webdriver', self._user_data['navigator.webdriver']),
            # ('platform', self._user_data['platform']), # Field gets collected but never actually used
            ('ActiveXObject', self._user_data['ActiveXObject']),
            ('webkitURL', self._user_data['webkitURL']),
            ('_phantom', self._user_data['_phantom']),
            ('callPhantom', self._user_data['callPhantom']),
            ('chrome', self._user_data['chrome']),
            ('yandex', self._user_data['yandex']),
            ('opera', self._user_data['opera']),
            ('opr', self._user_data['opr']),
            ('safari', self._user_data['safari']),
            ('awesomium', self._user_data['awesomium']),
            ('puffinDevice', self._user_data['puffinDevice']),
            ('__nightmare', self._user_data['__nightmare']),
            ('domAutomation', self._user_data['domAutomation']),
            ('domAutomationController', self._user_data['domAutomationController']),
            ('_Selenium_IDE_Recorder', self._user_data['_Selenium_IDE_Recorder']),
            ('document.__webdriver_script_fn', self._user_data['document.__webdriver_script_fn']),
            ('document.$cdc_asdjflasutopfhvcZLmcfl_', self._user_data['document.$cdc_asdjflasutopfhvcZLmcfl_']),
            ('process.version', self._user_data['process.version']),
            ('global.require', self._user_data['global.require']),
            ('global.process', self._user_data['global.process']),
            ('WebAssembly', self._user_data['WebAssembly']),
            ("require('fs')", self._user_data["require('fs')"]),
            ('globalThis==global', self._user_data['globalThis==global']),
            ('window.toString()', self._user_data['window.toString()']),
            ('navigator.cpuClass', self._user_data['navigator.cpuClass']),
            ('navigator.oscpu', self._user_data['navigator.oscpu']),
            ('navigator.connection', self._user_data['navigator.connection']),
            ("navigator.language=='C'", self._user_data["navigator.language=='C'"]),
            ('Object.keys(window).length', self._user_data['Object.keys(window).length']),
            ('window.outerWidth==0', self._user_data['window.outerWidth==0']),
            ('window.outerHeight==0', self._user_data['window.outerHeight==0']),
            ('window.WebGLRenderingContext', self._user_data['window.WebGLRenderingContext']),
            ('window.constructor.toString()', self._user_data['window.constructor.toString()']),
            ("Boolean(typeof process !== 'undefined' && process.versions && process.versions.node)", self._user_data["Boolean(typeof process !== 'undefined' && process.versions && process.versions.node)"]),
            ('document.documentMode', self._user_data['document.documentMode']),
            ('eval.toString().length', self._user_data['eval.toString().length']),
            ('navigator.connection.rtt', self._user_data['navigator.connection.rtt']),
            ('deviceType', self._user_data['deviceType']),
            ('screen.width', self._user_data['screen.width']),
            ('screen.height', self._user_data['screen.height']),
            ('eoapi', self._user_data['eoapi']),
            ('eoapi_VerifyThis', self._user_data['eoapi_VerifyThis']),
            ('eoapi_extInvoke', self._user_data['eoapi_extInvoke']),
            ('eoWebBrowserDispatcher', self._user_data['eoWebBrowserDispatcher']),
            ('window.HIDDEN_CLASS', self._user_data['window.HIDDEN_CLASS']),
            ('navigator.mimeTypes.length==2', self._user_data['navigator.mimeTypes.length==2']),
            ('navigator.plugins.length==2', self._user_data['navigator.plugins.length==2']),
            ('window.globalThis', self._user_data['window.globalThis']),
            ('navigator.userAgentData.brands[0].brand', self._user_data['navigator.userAgentData.brands[0].brand']),
            ('navigator.userAgentData.brands[1].brand', self._user_data['navigator.userAgentData.brands[1].brand']),
            ('navigator.userAgentData.brands[2].brand', self._user_data['navigator.userAgentData.brands[2].brand']),
            ("navigator.plugins('Microsoft Edge PDF Plugin')", self._user_data["navigator.plugins['Microsoft Edge PDF Plugin']"])
        ]
        
        formattedData: str = urllib.parse.quote(
            ''.join(['='.join(tups) for tups in data])
        )
        
        self.print_message('Generated user data.')
        return formattedData
       
    def rc4Decrypt_old(self, secret: str, encodedWord: str) -> str:
        """ Refactored js code into python code, copied original varnames """

        # Initialize vars
        _0x1847ad: list = list(range(0, 256))
        _0x47a6be: int = 0
        _0x576661: str = ''
        _0x4f0568: str = ''
        
        # Base64 decode and convert bytes to utf8
        encoded_word_bytes: str = base64.b64decode(encodedWord).decode('latin1')

        for i in range(0, 256):
            _0x47a6be = ( _0x47a6be + _0x1847ad[i] + ord(secret[i % len(secret)]) ) % 256 
            _0x576661 = _0x1847ad[i]
            _0x1847ad[i] = _0x1847ad[_0x47a6be]
            _0x1847ad[_0x47a6be] = _0x576661
        
        _0x4f9ca8 = 0
        _0x47a6be = 0
        for i in range(len(encoded_word_bytes)):
            _0x4f9ca8 = (_0x4f9ca8 + 1) % 256
            _0x47a6be = (_0x47a6be + _0x1847ad[_0x4f9ca8]) % 256
            _0x576661 = _0x1847ad[_0x4f9ca8]
            _0x1847ad[_0x4f9ca8] = _0x1847ad[_0x47a6be]
            _0x1847ad[_0x47a6be] = _0x576661
            _0x4f0568 += chr(
                ord(encoded_word_bytes[i]) ^ _0x1847ad[(_0x1847ad[_0x4f9ca8] + _0x1847ad[_0x47a6be]) % 256]
            );
            
        return _0x4f0568
    
    def rc4Decrypt(self, key: str, string: str) -> str:
        """ Refactored js rc4 decrypt/encrypt function into python function """
        
        s: list = list(range(0, 256))
        j: int = 0
        x: str = ''
        res: str = ''
        
        for i in range(0, 256):
            j = (j + s[i] + ord(key[i % len(key)])) % 256
            x = s[i]
            s[i] = s[j]
            s[j] = x
            
        i = 0
        j = 0
        for y in range(len(string)):
            i = (i + 1) % 256
            j = (j + s[i]) % 256
            x = s[i]
            s[i] = s[j]
            s[j] = x
            res += chr(
                ord(string[y]) ^ s[(s[i] + s[j]) % 256]
            )
            
        return res
       
    def create_cookie(self, secret_cookie_key: str) -> str:
        """ Encodes the cookie """
        
        encoded_user_data = self.rc4Decrypt(
            secret_cookie_key[0:5],
            self.create_data()
        )
        
        for (cookie_name, cookie_value) in self._session.cookies.get_dict().items():
            if 'incap_ses_' in cookie_name:
                incap_ses_cookie_value: str = cookie_value

        digest: str = self.generate_digest(incap_ses_cookie_value, encoded_user_data)
        s_value: str = self.generate_s_value(secret_cookie_key, digest)
        
        cookie: str = '{encoded_user_data},digest={digest},s={s}'.format(
            encoded_user_data=encoded_user_data,
            digest=digest,
            s=s_value
        )
        
        cookie_encoded: str = base64.standard_b64encode(cookie.encode('latin1')).decode('latin1')
        
        self.print_message(f'Generated cookie: {cookie_encoded}')
        return cookie_encoded# Encoding in latin1 is needed!
    
    def generate_digest(self, incap_sess_cookie_value: str, generated_data: str) -> str:
        """ Generates the digist that is needed in the cookie """
        total_digest_string: str = generated_data + incap_sess_cookie_value
        
        digest = 0
        for char in total_digest_string:
            digest += ord(char)
        
        self.print_message(f'Generated digest: {digest}')
        return str(digest)
    
    def generate_s_value(self, cookie_secret: str, digest: str) -> str:
        s_value: str = ''
        
        for i in range(len(cookie_secret)):
            s_value += str(hex(
                ord(cookie_secret[i]) + ord(digest[i % len(digest)])
            ))[-2:]
            
        self.print_message(f'Generated s value: {s_value}')
        return s_value
       
if __name__ == '__main__':
    IncapsulaGen(
        requests.Session(),
        {
            'navigator.userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
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
        },
        True
    ).solve_challenge(
        'https://www.smythstoys.com/_Incapsula_Resource?SWJIYLWA=719d34d31c8e3a6e6fffd425f7e032f3'
    )