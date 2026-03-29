// modules/logger.js

function timestamp() {
  return new Date().toLocaleTimeString("pt-PT");
}

export const log = {
  info(msg) {
    console.info(`[INFO ${timestamp()}] ${msg}`);
  },

  warn(msg) {
    console.warn(`[WARN ${timestamp()}] ${msg}`);
  },

  error(msg) {
    console.error(`[ERROR ${timestamp()}] ${msg}`);
  },

  debug(msg) {
    if (window.env === "development") {
      console.debug(`[DEBUG ${timestamp()}] ${msg}`);
    }
  }
};
