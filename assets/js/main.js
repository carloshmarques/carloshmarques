'use strict';

import { Core } from "./modules/core.js";
import { initNavigation } from "./modules/navigation.js";
import { Theme } from "./theme.js";
import { log } from "./modules/logger.js";

document.addEventListener("DOMContentLoaded", () => {
  document.documentElement.classList.add("ready");

  log.info("Sistema iniciado");

  Core.init();
  Theme.init();
  initNavigation();

  log.info("Document ready for code injection");
});



