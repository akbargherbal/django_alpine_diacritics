// app.js
import Alpine from "./node_modules/alpinejs/dist/module.esm.js";
import {
  wordNavigator,
  charNavigator,
  addDiaByLocalIndex,
  addDiaByGlobalIndex,
  clearSelections,
} from "./utils.js";
import { setupHotkeys } from "./hotkeys.js";
import { logFunctionCall } from "./logger.js";

window.Alpine = Alpine;

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
    mode: "",

    // New method to update dictionaries and state
    updateDictionariesAndState() {
      // Update dictionaries
      window.wd_dict = JSON.parse(
        document.getElementById("wd_dict").textContent
      );
      window.char_dict_global = JSON.parse(
        document.getElementById("char_dict_global").textContent
      );
      window.char_dict_local = JSON.parse(
        document.getElementById("char_dict_local").textContent
      );

      // Update component state
      this.tokensCount = parseInt(
        document.querySelector(".verse").getAttribute("data-tokens-count")
      );
      this.totalDiacritics = parseInt(
        document.querySelector(".verse").getAttribute("data-dia-count")
      );
      this.mode = document.querySelector(".verse").getAttribute("data-mode");

      // Reset selection state
      this.wordIsSelected = false;
      this.wordIndex = -1;
      this.charIndex = -1;
      this.globalDiaIndex = 0;
      this.isEditMode = false;
      this.isAutoPilot = false;

      // Clear any visual selections
      clearSelections();

      // Debug logging
      console.log("State updated:", {
        tokensCount: this.tokensCount,
        totalDiacritics: this.totalDiacritics,
        mode: this.mode
      });
    },

    init() {
      console.log("Alpine initialized");
      
      // Initial setup
      this.updateDictionariesAndState();

      // Listen for HTMX updates
      document.body.addEventListener('htmx:afterSettle', () => {
        console.log("HTMX update detected");
        this.updateDictionariesAndState();
      });

      // Set up hotkeys
      const functionPackage = {
        wordNavigator: () => this.wordNavigator(),
        charNavigator: () => this.charNavigator(),
        addDia: () => this.addDia(),
        toggleEditMode: () => this.toggleEditMode(),
        toggleAutoPilot: () => this.toggleAutoPilot(),
      };

      setupHotkeys(functionPackage);

      // Watch for state changes
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
      this.isAutoPilot = true;
      this.isEditMode = false;
      this.addDia(this, event);
      console.log(
        `isAutoPilot: ${this.isAutoPilot}; isEditMode: ${this.isEditMode}; globalDiaIndex: ${this.globalDiaIndex}`
      );
    },

    wordNavigator() {
      if (!this.isEditMode) return;
      if (this.isAutoPilot) return; // Disable in auto-pilot mode
      wordNavigator(this);
    },

    charNavigator() {
      if (!this.isEditMode) return;
      if (this.isAutoPilot) return; // Disable in auto-pilot mode
      charNavigator(this);
    },

    addDia() {
      if (this.isAutoPilot) {
        addDiaByGlobalIndex(this, event);
      } else {
        if (!this.isEditMode) {
          return;
        }
        addDiaByLocalIndex(this, event);
      }
    },
  }));
});

Alpine.start();