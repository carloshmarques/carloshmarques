'use strict';
var logger = require('./modules/logger');
var core = require('./modules/core');

// Mensagem inicial
logger.log("User successfully authenticated, profile ready!");

// Quando o documento estiver pronto
$(document).ready(function () {

    // Frase aleatória do core
    const frase = core.frases[Math.floor(Math.random() * core.frases.length)];
    core.log(frase);

    // Mensagem final
    console.log('Document ready for code injection!');
});

