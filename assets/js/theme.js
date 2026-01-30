import { Events } from "./modules/events.js";
import { log } from "./modules/logger.js";

export const Theme = {
  key: "cm-theme",

  get() {
    return localStorage.getItem(this.key) || "dark";
  },

  apply(theme) {
    document.body.className = `${theme}-theme`;
    localStorage.setItem(this.key, theme);
    Events.emit("themeChanged", theme);
    log.info(`Tema aplicado: ${theme}`);
  },

  init() {
    const saved = this.get();
    this.apply(saved);
    log.info("Sistema de temas inicializado");
  }
};

