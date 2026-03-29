'use strict';

import { Events } from "./modules/events.js";
import { log } from "./modules/logger.js";

export const Theme = {
  key: "sk-theme",

  get() {
    return localStorage.getItem(this.key) || "dark";
  },

  apply(theme) {
    const themes = [
      "light-theme", "dark-theme", "solarized-theme", 
      "dracula-theme", "hydra-theme", "neon-theme"
    ];

    document.documentElement.classList.remove(...themes);
    document.documentElement.classList.add(`${theme}-theme`);
    localStorage.setItem(this.key, theme);

    const el = document.querySelector(".hero_description--last");
    if (el) {
      el.classList.remove("animate");
      void el.offsetWidth; // força reflow
      el.classList.add("animate");
    }

    Events.emit("themeChanged", theme);
    log.info(`Tema aplicado: ${theme}`);
  },

  init() {
    const saved = this.get();
    this.apply(saved);
    log.info("Sistema de temas inicializado");
  }
};
