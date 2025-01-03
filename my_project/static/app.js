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
    isEditMode: false,

    init() {
      setupHotkeys({
        wordNavigator: () => this.wordNavigator(),
        charNavigator: () => this.charNavigator(),
        addDia: () => this.addDia(),
        toggleEditMode: (event) => this.toggleEditMode(event),
      });

      this.tokensCount = parseInt(
        document.querySelector(".verse").getAttribute("data-tokens-count")
      );

      this.$watch("wordIndex", (value, oldValue) => {
        console.table({
          wordIndex: this.wordIndex,
          tokensCount: this.tokensCount,
          editMode: this.isEditMode,
          currentDia: this.currentDia,
        });
      });
    },

    wordNavigator() {
      if (!this.isEditMode) return;
      wordNavigator(this);
    },

    charNavigator() {
      if (!this.isEditMode) return;
      charNavigator(this);
    },

    addDia() {
      if (!this.isEditMode) return;
      addDia(this, event);
    },

    toggleEditMode(event) {
      if (["Enter", "Space"].includes(event.code)) {
        this.isEditMode = true;
      }

      if (event.code === "Escape") {
        this.isEditMode = false;
      }
    },
  }));
});

Alpine.start();
