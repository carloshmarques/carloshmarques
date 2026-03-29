import { log } from "./logger.js";

export const Core = {
  frases: [
    "A mente que se abre a uma nova ideia jamais volta ao seu tamanho original.",
    "O código é poesia.",
    "Cada ritual técnico é um passo para a autonomia.",
    "A arquitetura é o destino do software."
  ],

  getRandomFrase() {
    const i = Math.floor(Math.random() * this.frases.length);
    return this.frases[i];
  },

  init() {
    const frase = this.getRandomFrase();
    log.info(`Core initialized → ${frase}`);
  }
};

