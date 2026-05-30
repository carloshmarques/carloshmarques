import { Theme } from "../theme.js";
import { log } from "./logger.js";

export function initNavigation() {
  const menuBtn = document.querySelector(".menu-btn");
  const nav = document.querySelector(".menu-nav");

  if (!menuBtn || !nav) {
    log.warn("NAV não encontrada no DOM");
    return;
  }

  // Hambúrguer
  menuBtn.addEventListener("click", () => {
    nav.classList.toggle("open");
    menuBtn.classList.toggle("open");
  });

  // Dropdown de temas
  const themeLinks = document.querySelectorAll(".dropdown-menu a");

  themeLinks.forEach(link => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      const theme = link.textContent.trim();
      Theme.apply(theme);
    });
  });

  log.info("NAV inicializada");
}
