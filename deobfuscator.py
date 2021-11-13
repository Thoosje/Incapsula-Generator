""" This code is fucking ugly, ignore it pls"""

from typing import Iterator, Any

import re
import js2py
import base64

class Incapsula_Deobfuscator():
    def __init__(self, debug: bool) -> None:        
        self.debug = debug    
        
    def print_message(self, message: str) -> None:
        if self.debug:
            print(f'[DEOBFUSCATOR] {message}')
            
    def convert_into_js_string(self, input_string: str) -> str:
        if "'" in input_string:
            return f'`{input_string}`'
        else:
            return f"'{input_string}'"
    
    def deob_script(self, script: str) -> str:
        self.print_message('Deobfuscating script\n---------')
        
        script = self.decode_script(script)
        script = self.remove_byte_strings(script)
        (words, wordArray) = self.find_word_array(script)

        script = self.replace_decoded_words(script, words)

        script = self.find_proxy_dicts(script)
    
        script = wordArray + '\n' + script
        return script
    
    def decode_script(self, script: str) -> str:
        self.print_message('Converting encdoded script to readable script')
        
        varB: str = script.split('b="')[1].split('"')[0]
        script = ''
        
        counter: int = 0
        while counter < len(varB):
            script = script + chr(int(
                varB[counter:(counter + 2)], 16
            ))
            
            counter = counter + 2
        
        self.print_message('Decoded initial script!')
        
        return script
    
    def remove_byte_strings(self, script: str) -> str:
        self.print_message('Removing byte strings.')   
        
        matches: Iterator = re.finditer(r"'\\x(.*?)'", script, re.MULTILINE)
        for _, match in enumerate(matches, start=1):
            escaped_string: str = match.group().replace("'", '')
            unescaped_string: str = js2py.eval_js(f'unescape("{str(escaped_string)}")')
        
            script = script.replace(
                f"'{escaped_string}'", 
                self.convert_into_js_string(unescaped_string)
            )
            
        return script
    
    def find_word_array(self, script: str ) -> tuple[list[str], str]:
        self.print_message('Searching for word array')
        
        matches: Any = re.search(r"var (.*?)=\[(?:['`](.*?)['`])*?\];", script, re.MULTILINE)
        varName: str = matches.group(1)
        word_array: list[str] = matches.group(2).split("','")
        
        self.secret_int: str = script.split(f'({varName},')[1].split(')')[0]
        
        # Shifts array
        for i in range(int(self.secret_int, 16), 0, -1):
            word_array.append(word_array.pop(0))
       
        return (word_array, matches.group())
    
    def find_encode_string_func_name(self, script: str) -> str:
        return script.split(self.secret_int)[1].split('var ')[1].split('=')[0]
    
    def replace_decoded_words(self, script: str, words: list[str]) -> str:
        self.print_message('Searching for encoded words')
        
        funcName: str = self.find_encode_string_func_name(script)        
        matches: Iterator = re.finditer(fr"{funcName}\('(.*?)', '(.*?)'\)", script, re.MULTILINE)
        
        for _, match in enumerate(matches, start=1):
            try:
                encoded_word: str = match.group()
                encoded_word_index: int = int(match.group(1), 16)
                encoded_word_secret: str = match.group(2)
                
                decoded_word = self.rc4Decrypt(encoded_word_index, encoded_word_secret, words)
                
                script = script.replace(encoded_word, self.convert_into_js_string(decoded_word))
            except Exception:
                self.print_message('Special encoded word found.')
                
                encoded_word = match.group().split(')')[0] + ')'
                encoded_word_index = int(match.group(1).split("',")[0], 16)
                encoded_word_secret = encoded_word.split(',')[1].split(')')[0].strip()

                generate_needed_data_code: list[str] = list(reversed(script.split(encoded_word)[0].split('case')))[0].split(':')
                del generate_needed_data_code[0]
                generate_needed_data_code = (':'.join(generate_needed_data_code)).split('var')
                del generate_needed_data_code[len(generate_needed_data_code) - 1]
                
                generate_needed_data_code_final: str = 'var'.join(generate_needed_data_code)
                
                encoded_word_secret = js2py.eval_js(f'{generate_needed_data_code_final} {encoded_word_secret}')
                decoded_word = self.rc4Decrypt(encoded_word_index, encoded_word_secret, words)
                    
                script = script.replace(encoded_word, self.convert_into_js_string(decoded_word))
            
        self.print_message('Removed encoded words')
        
        return script
    

    def rc4Decrypt(self, place: int, secret: str, wordArray: list[str]) -> str:
        """ Refactored js code into python code, copied original varnames """
        
        encodedWord: str = wordArray[place]

        # Initialize vars
        _0x1847ad: list = list(range(0, 256))
        _0x47a6be: int = 0
        _0x576661: str = ''
        _0x4f0568: str = ''
        
        # Base64 decode and convert bytes to utf8
        encoded_word_bytes: str = base64.b64decode(encodedWord).decode('utf8')

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
            )
            
        return _0x4f0568
    
    def find_proxy_dicts(self, script: str) -> str:
        self.print_message('Searching for proxy functions and parsing them')
        
        matches: Iterator = re.finditer(r"var _0x((?=\d+[A-Za-z]+[\w@]+|[a-zA-Z]+[\w@]+)[\w@]{6})={(.*?)};", script, re.MULTILINE)
        for _, match in enumerate(matches, start=1):
            total_proxy_dict: str = match.group()
            
            if 'cookie' in total_proxy_dict:
                continue
            
            original_proxy_dict_var: str = f'_0x{match.group(1)}'
            proxy_dicts: Iterator = re.finditer(r"'([a-zA-Z]{3})':function .*?\((.*?)\){return (.*?);}", total_proxy_dict, re.MULTILINE)
            
            for _, matchInside in enumerate(proxy_dicts, start=1):
                proxy_dict_name: str = matchInside.group(1)
                proxy_dict_params: list[str] = matchInside.group(2).split(',')
                proxy_dict_output: str = matchInside.group(3)
            
                while True:
                    allCases: list[str] = script.split(f"{original_proxy_dict_var}['{proxy_dict_name}']")
                    allCases.pop(0)
                    
                    if len(allCases) == 0:
                        break
                    for case in allCases:
                        brackets: dict[str, int] = {
                            'open': 0,
                            'closed': 0
                        }
                        
                        inputVars: list = []
                        proxy_dict_input: str = ''
                        
                        i: int = 0
                        lastIndexParam: int = i + 1
                        
                        for char in case:
                            i = i + 1

                            proxy_dict_input += char
                            
                            if char == ')':
                                brackets['closed'] += 1
                                
                                if brackets['closed'] == brackets['open']:
                                    if len(inputVars) == 0:
                                        inputVars.append(proxy_dict_input.replace('(', '').replace(')', ''))
                                    else:
                                        lastInput = proxy_dict_input.replace(f"({','.join(inputVars)},", '')[:-1]          
                                        inputVars.append(lastInput)

                                    correctionCounter: int = 0
                                    for inputVar in inputVars:
                                        if inputVar == "'":
                                            inputVars[correctionCounter + 1] = "'" + inputVars[correctionCounter + 1]
                                            del inputVars[correctionCounter]
                
                                        correctionCounter += 1

                                    correct_output: str = proxy_dict_output
                                    for i in range(len(proxy_dict_params)):
                                        correct_output = correct_output.replace(proxy_dict_params[i], inputVars[i])
                                    
                                    script = script.replace(f"{original_proxy_dict_var}['{proxy_dict_name}']{proxy_dict_input}", correct_output)
                                    break
                            elif char == '(':
                                brackets['open'] += 1
                            elif char == ',':
                                if brackets['closed'] == brackets['open'] - 1:
                                    inputVars.append(proxy_dict_input[lastIndexParam:i - 1])
                                    lastIndexParam = i
                                    
        return script