const encodeDataField = ( data ) => {
    let splittedData = data.split('=');

    return {
        'fieldName': data.replace(`=${splittedData[splittedData.length - 1]}`, ''),
        'value': splittedData[splittedData.length - 1],
    }
};

const generetaData = ( fields ) => {
    var gennedData = {};
       
    for (var counter = 0; counter < fields.length; counter++) {
        var fieldName = fields[counter][0];

        switch (fields[counter][1]) {
            case 'exists':
                try {
                    if (typeof window.eval(fieldName) !== 'undefined') {
                        gennedData[fieldName] = 'true';
                    } else {
                        gennedData[fieldName] = 'false';
                    }
                } catch ( error ) {
                    gennedData[fieldName] = 'false';
                }
                break;
            case 'value':
                try {
                    try {
                        let value = window.eval(fieldName);
                        if (typeof value === 'undefined') {
                            gennedData[fieldName] = 'undefined';
                        } else if (value === null) {
                            gennedData[fieldName] = 'null';
                        } else {
                            gennedData[fieldName] = value.toString();
                        }
                    } catch ( error ) {
                        gennedData[fieldName] = 'cannot evaluate';
                        break;
                    }
                    break;
                } catch ( error ) {
                    gennedData[fieldName] = '' + error;
                }
                break;
            case 'plugin_extentions':
                try {
                    var plugin_ext = [];
                    try {
                        value = plugin_ext['indexOf']('i');
                    } catch ( error ) {
                        gennedData['plugin_ext'] = 'indexOf is not a function';
                        break;
                    }

                    try {
                        var plugins_length = window.navigator.plugins.length;
                        if (plugins_length == 0 || plugins_length == null) {
                            gennedData['plugin_ext'] = 'no plugins';
                            break;
                        }
                    } catch ( error ) {
                        gennedData['plugin_ext'] = 'cannot evaluate';
                        break;
                    }
                    
                    for (var counter_plugins = 0; counter_plugins < window.navigator.plugins.length; counter_plugins++) {
                        if (typeof window.navigator.plugins[counter_plugins] === 'undefined') {
                            gennedData['plugin_ext'] = 'plugins[i] is undefined';
                            break;
                        }

                        var plugin_filename = window.navigator.plugins[counter_plugins]['filename'];
                        var plugin_ext_name = 'no extention';

                        if (typeof plugin_filename === 'undefined') {
                            plugin_ext_name = 'filename is undefined';
                        } else if (plugin_filename['split']('.').length > 1) {
                            plugin_ext_name = plugin_filename['split']('.')['pop']();
                        }

                        if (plugin_ext['indexOf'](plugin_ext_name) < 0) {
                            plugin_ext['push'](plugin_ext_name);
                        }
                    }
                    
                    for (var counter_plugins = 0; counter_plugins < plugin_ext.length; counter_plugins++) {
                        gennedData['plugin_ext'] = '' + plugin_ext[counter_plugins];
                    }
                } catch ( error ) {
                    gennedData['plugin_ext'] = '' + error;
                }
                break;
            case 'function':
                if (fieldName === 'deviceType') {
                    try {
                        var user_type = '';

                        if (/(tablet|ipad|playbook|silk)|(android(?!.*mobi))/i ['test'](navigator.userAgent)) {
                            user_type = 'tablet';
                        } else if (/Mobile|iP(hone|od|ad)|Android|BlackBerry|IEMobile|Kindle|Silk-Accelerated|(hpw|web)OS|Opera M(obi|ini)/ ['test'](navigator.userAgent)) {
                            user_type = 'mobile';
                        } else {
                            user_type = 'desktop';
                        }

                        gennedData[fieldName] = user_type.toString();
                    } catch ( error ) {
                        gennedData[fieldName] = 'cannot evaluate' + error.toString();
                    }
                }
                break;
        }
    
    }
    return gennedData
}

let collectedData = generetaData([
    ['navigator', 'exists'],
    ['navigator.vendor', 'value'],
    ['navigator.appName', 'value'],
    ['navigator.plugins.length==0', 'value'],
    ['navigator.platform', 'value'],
    ['navigator.webdriver', 'value'],
    ['platform', 'plugin_extentions'],
    ['ActiveXObject', 'exists'],
    ['webkitURL', 'exists'],
    ['_phantom', 'exists'],
    ['callPhantom', 'exists'],
    ['chrome', 'exists'],
    ['yandex', 'exists'],
    ['opera', 'exists'],
    ['opr', 'exists'],
    ['safari', 'exists'],
    ['awesomium', 'exists'],
    ['puffinDevice', 'exists'],
    ['__nightmare', 'exists'],
    ['domAutomation', 'exists'],
    ['domAutomationController', 'exists'],
    ['_Selenium_IDE_Recorder', 'exists'],
    ['document.__webdriver_script_fn', 'exists'],
    ['document.$cdc_asdjflasutopfhvcZLmcfl_', 'exists'],
    ['process.version', 'exists'],
    ['global.require', 'exists'],
    ['global.process', 'exists'],
    ['WebAssembly', 'exists'],
    [`require('fs')`, 'exists'],
    ['globalThis==global', 'value'],
    ['window.toString()', 'value'],
    ['navigator.cpuClass', 'exists'],
    ['navigator.oscpu', 'exists'],
    ['navigator.connection', 'exists'],
    [`navigator.language=='C'`, 'value'],
    ['Object.keys(window).length', 'value'],
    ['window.outerWidth==0', 'value'],
    ['window.outerHeight==0', 'value'],
    ['window.WebGLRenderingContext', 'exists'],
    ['window.constructor.toString()', 'value'],
    [`Boolean(typeof process !== 'undefined' && process.versions && process.versions.node)`, 'value'],
    ['document.documentMode', 'value'],
    ['eval.toString().length', 'value'],
    ['navigator.connection.rtt', 'value'],
    ['deviceType', 'function'],
    ['screen.width', 'value'],
    ['screen.height', 'value'],
    ['eoapi', 'exists'],
    ['eoapi_VerifyThis', 'exists'],
    ['eoapi_extInvoke', 'exists'],
    ['eoWebBrowserDispatcher', 'exists'],
    ['window.HIDDEN_CLASS', 'exists'],
    ['navigator.mimeTypes.length==2', 'value'],
    ['navigator.plugins.length==2', 'value'],
    ['window.globalThis', 'exists'],
    ['navigator.userAgentData.brands[0].brand', 'value'],
    ['navigator.userAgentData.brands[1].brand', 'value'],
    ['navigator.userAgentData.brands[2].brand', 'value'],
    [`navigator.plugins['Microsoft Edge PDF Plugin']`, 'exists']
]);

document.getElementById('collectedData').innerHTML = JSON.stringify(collectedData);