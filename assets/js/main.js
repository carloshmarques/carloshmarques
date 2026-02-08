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

  // ---------------------------------------------------------
  // Função de scroll suave com easing
  // ---------------------------------------------------------
  const smoothScrollTo = (targetY, duration = 900) => {
    const startY = window.scrollY;
    const diff = targetY - startY;
    let start;

    const step = (timestamp) => {
      if (!start) start = timestamp;
      const time = timestamp - start;
      const percent = Math.min(time / duration, 1);

      // Ease-out cubic
      const easing = 1 - Math.pow(1 - percent, 3);

      window.scrollTo(0, startY + diff * easing);

      if (time < duration) requestAnimationFrame(step);
    };

    requestAnimationFrame(step);
  };

  // ---------------------------------------------------------
  // Smooth Reveal da section-home
  // ---------------------------------------------------------
  const exploreBtn = document.querySelector(".hero_btn");
  const homeSection = document.querySelector("#home");

  if (exploreBtn && homeSection) {
    exploreBtn.addEventListener("click", (e) => {
      e.preventDefault();

      // Mostrar a secção
      homeSection.classList.add("visible");
      exploreBtn.classList.add("hidden");

      // Scroll suave
      const targetY = homeSection.getBoundingClientRect().top + window.scrollY;
      smoothScrollTo(targetY, 2000);

    });
  }

  log.info("Document ready for code injection");
});

 

