import Alpine from "./node_modules/alpinejs/dist/module.esm.js";
import { diacritics, ar_alpha } from "./data.js";
import {
  wordNavigator,
  charNavigator,
  handleDiacritics,
  logEvent,
} from "./utils.js";

window.Alpine = Alpine;
window.logEvent = logEvent;

document.addEventListener("alpine:init", () => {
  Alpine.data("sentHook", () => ({
    wordIndex: -1,
    wordSelected: false,
    charIndex: 0,
    currentDia: "",
    diaIndex: 0,
    dia: ["", ""],
    maxDia: 2,
    tokensCount: 0,
    init() {
      console.log("Available diacritics:", diacritics);

      // get value of data-tokens-count
      this.tokensCount = document
        .querySelector(".verse")
        .getAttribute("data-tokens-count");
      this.tokensCount = parseInt(this.tokensCount);

      this.$watch("wordIndex", (value, oldValue) => {
        console.table({
          wordIndex: this.wordIndex,
          tokensCount: this.tokensCount,
          wordSelected: this.wordSelected,
        });
      });
    },

    handleKeyDown(event) {
      if (event.ctrlKey && event.code === "Space") {
        event.preventDefault();
        wordNavigator(this);
      }

      if (!event.ctrlKey && event.code === "Space") {
        event.preventDefault();
        charNavigator(this);
      }

      if (diacritics.includes(event.key)) {
        handleDiacritics(event, this);
      }
    },
  }));
});

Alpine.start();
