(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
'use strict';
var logger = require('./modules/logger');
var core = require('./modules/core');

// Mensagem inicial
logger.log("Visitor successfully authenticated, profile ready!");

// Quando o documento estiver pronto
$(document).ready(function () {

    // Frase aleatória do core
    const frase = core.frases[Math.floor(Math.random() * core.frases.length)];
    core.log(frase);

    // Mensagem final
    console.log('Document ready for code injection!');
});


},{"./modules/core":2,"./modules/logger":3}],2:[function(require,module,exports){
module.exports = {
    log: function (msg) {
        if (console) console.log(msg);
    },

    frases: [
        "Sistema acordado.",
        "Ambiente carregado com sucesso.",
        "Tudo operacional.",
        "Pronto para mais um ritual técnico.",
        "Código alinhado e consciente."
    ]
};
},{}],3:[function(require,module,exports){
module.exports = {
    log: function(string) {
        if (console) console.log(string);
    }
};


},{}]},{},[1]);

//# sourceMappingURL=main.js.map
