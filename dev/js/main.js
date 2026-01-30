(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
'use strict';

var _core = require("./modules/core.js");
var _navigation = require("./modules/navigation.js");
var _theme = require("./theme.js");
var _logger = require("./modules/logger.js");
document.addEventListener("DOMContentLoaded", function () {
  _logger.log.info("Sistema iniciado");
  _core.Core.init();
  _theme.Theme.init();
  (0, _navigation.initNavigation)();
  _logger.log.info("Document ready for code injection");
});

},{"./modules/core.js":2,"./modules/logger.js":4,"./modules/navigation.js":5,"./theme.js":6}],2:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.Core = void 0;
var _logger = require("./logger.js");
var Core = exports.Core = {
  frases: ["A mente que se abre a uma nova ideia jamais volta ao seu tamanho original.", "O código é poesia.", "Cada ritual técnico é um passo para a autonomia.", "A arquitetura é o destino do software."],
  getRandomFrase: function getRandomFrase() {
    var i = Math.floor(Math.random() * this.frases.length);
    return this.frases[i];
  },
  init: function init() {
    var frase = this.getRandomFrase();
    _logger.log.info("Core initialized \u2192 ".concat(frase));
  }
};

},{"./logger.js":4}],3:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.Events = void 0;
var Events = exports.Events = {
  events: {},
  on: function on(event, handler) {
    if (!this.events[event]) this.events[event] = [];
    this.events[event].push(handler);
  },
  emit: function emit(event, data) {
    if (!this.events[event]) return;
    this.events[event].forEach(function (handler) {
      return handler(data);
    });
  }
};

},{}],4:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.log = void 0;
// modules/logger.js

function timestamp() {
  return new Date().toLocaleTimeString("pt-PT");
}
var log = exports.log = {
  info: function info(msg) {
    console.info("[INFO ".concat(timestamp(), "] ").concat(msg));
  },
  warn: function warn(msg) {
    console.warn("[WARN ".concat(timestamp(), "] ").concat(msg));
  },
  error: function error(msg) {
    console.error("[ERROR ".concat(timestamp(), "] ").concat(msg));
  },
  debug: function debug(msg) {
    if (window.env === "development") {
      console.debug("[DEBUG ".concat(timestamp(), "] ").concat(msg));
    }
  }
};

},{}],5:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.initNavigation = initNavigation;
var _theme = require("../theme.js");
var _logger = require("./logger.js");
function initNavigation() {
  var menuBtn = document.querySelector(".menu-btn");
  var nav = document.querySelector(".menu-nav");
  if (!menuBtn || !nav) {
    _logger.log.warn("NAV não encontrada no DOM");
    return;
  }

  // Hambúrguer
  menuBtn.addEventListener("click", function () {
    nav.classList.toggle("open");
    menuBtn.classList.toggle("open");
  });

  // Dropdown de temas
  var themeLinks = document.querySelectorAll(".dropdown-menu a");
  themeLinks.forEach(function (link) {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      var theme = link.textContent.trim();
      _theme.Theme.apply(theme);
    });
  });
  _logger.log.info("NAV inicializada");
}

},{"../theme.js":6,"./logger.js":4}],6:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.Theme = void 0;
var _events = require("./modules/events.js");
var _logger = require("./modules/logger.js");
var Theme = exports.Theme = {
  key: "cm-theme",
  get: function get() {
    return localStorage.getItem(this.key) || "dark";
  },
  apply: function apply(theme) {
    document.body.className = "".concat(theme, "-theme");
    localStorage.setItem(this.key, theme);
    _events.Events.emit("themeChanged", theme);
    _logger.log.info("Tema aplicado: ".concat(theme));
  },
  init: function init() {
    var saved = this.get();
    this.apply(saved);
    _logger.log.info("Sistema de temas inicializado");
  }
};

},{"./modules/events.js":3,"./modules/logger.js":4}]},{},[1])

//# sourceMappingURL=main.js.map
