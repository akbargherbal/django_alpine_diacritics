// app.js
import Alpine from "./node_modules/alpinejs/dist/module.esm.js";
import {
  wordNavigator,
  charNavigator,
  logEvent,
  addDiaByLocalIndex,
  addDiaByGlobalIndex,
  selectDiacriticByGlobalIndex,
  clearSelections,
} from "./utils.js";
import { setupHotkeys } from "./hotkeys.js";
import { logFunctionCall } from "./logger.js";


window.Alpine = Alpine;
window.logEvent = logEvent;

document.addEventListener("alpine:init", () => {
  Alpine.data("sentHook", () => ({
    wordIsSelected: false,
    wordIndex: -1,
    charIndex: -1,
    currentDia: "",
    isEditMode: false,
    isAutoPilot: false,
    globalDiaIndex: 0,
    totalDiacritics: 0,
    currentChar: "",

    init() {
      // Step 1: Create an object that packages all our functions
      logFunctionCall();
      const functionPackage = {
        wordNavigator: () => this.wordNavigator(),
        charNavigator: () => this.charNavigator(),
        addDia: () => this.addDia(),
        toggleEditMode: () => this.toggleEditMode(),
        toggleAutoPilot: () => this.toggleAutoPilot(),
      };

      // Step 2: Pass that package to setupHotkeys
      setupHotkeys(functionPackage);

      this.tokensCount = parseInt(
        document.querySelector(".verse").getAttribute("data-tokens-count")
      );

      this.totalDiacritics = parseInt(
        document.querySelector(".verse").getAttribute("data-dia-count")
      );

      this.$watch("wordIndex", (value, oldValue) => {
        console.table({
          wordIndex: this.wordIndex,
          tokensCount: this.tokensCount,
          isEditMode: this.isEditMode,
          isAutoPilot: this.isAutoPilot,
          globalDiaIndex: this.globalDiaIndex,
        });
      });
    },

    toggleEditMode() {
      logFunctionCall();
      if (event.key === "Enter") {
        this.isEditMode = true;
        this.isAutoPilot = false;
        wordNavigator(this);
        console.log(
          `isAutoPilot: ${this.isAutoPilot}; isEditMode: ${this.isEditMode}`
        );
      } else if (event.key === "Escape") {
        this.isEditMode = false;
        this.isAutoPilot = false;
        clearSelections();
      }
    },

    toggleAutoPilot() {
      logFunctionCall();
      this.isAutoPilot = true;
      this.isEditMode = false;
      this.selectDiacriticByGlobalIndex(this.globalDiaIndex);
      console.log(
        `isAutoPilot: ${this.isAutoPilot}; isEditMode: ${this.isEditMode}; globalDiaIndex: ${this.globalDiaIndex}`
      );
    },

    wordNavigator() {
      logFunctionCall();
      if (!this.isEditMode) return;
      if (this.isAutoPilot) return; // Disable in auto-pilot mode
      wordNavigator(this);
    },

    charNavigator() {
      logFunctionCall();
      if (!this.isEditMode) return;
      if (this.isAutoPilot) return; // Disable in auto-pilot mode
      charNavigator(this);
    },

    addDia() {
      logFunctionCall();
      if (this.isAutoPilot) {
        addDiaByGlobalIndex(this, event);
      } else {
        if (!this.isEditMode) {
          // console.trace("not in edit mode or autopilot mode; exiting!");
          return;
        }
        addDiaByLocalIndex(this, event);
        console.trace(`Current Dia ${this.currentDia}`);
      }
    },

    selectDiacriticByGlobalIndex(index) {
      logFunctionCall();
      selectDiacriticByGlobalIndex(index);
      //  method to highlight first character after isAutoPilot true;
    },
  }));
});

Alpine.start();
