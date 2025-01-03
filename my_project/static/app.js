// app.js
import Alpine from "./node_modules/alpinejs/dist/module.esm.js";
import { wordNavigator, charNavigator, logEvent, addDia } from "./utils.js";
import { setupHotkeys } from "./hotkeys.js";

window.Alpine = Alpine;
window.logEvent = logEvent;

document.addEventListener("alpine:init", () => {
  Alpine.data("sentHook", () => ({
    wordIndex: -1,
    charIndex: -1,
    currentDia: "",

    init() {
      setupHotkeys({
        wordNavigator: () => this.wordNavigator(),
        charNavigator: () => this.charNavigator(),
        addDia: () => this.addDia(),
      });

      this.tokensCount = parseInt(
        document.querySelector(".verse").getAttribute("data-tokens-count")
      );

      this.$watch("wordIndex", (value, oldValue) => {
        console.table({
          wordIndex: this.wordIndex,
          tokensCount: this.tokensCount,
        });
      });
    },

    wordNavigator() {
      wordNavigator(this);
    },

    charNavigator() {
      charNavigator(this);
    },

    addDia() {
      addDia(this, event);
    },
  }));
});

Alpine.start();
