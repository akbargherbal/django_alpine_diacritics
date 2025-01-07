// utils.js
import { DIACRITICS_CONFIG } from "./data.js";
import { logFunctionCall } from "./logger.js";
// ============================
// Core Navigation Functions
// ============================
export function normalizeIndex(index, maxLen) {
  logFunctionCall();
  if (index >= maxLen) return 0;
  if (index < 0) return maxLen - 1;
  return index;
}

export function clearSelections() {
  logFunctionCall();
  document.querySelectorAll("span").forEach((word) => {
    word.classList.remove("selected-word", "selected-char", "blinking-cursor");
  });
}

// ============================
// Word-Level Operations
// ============================
export function wordNavigator(state) {
  logFunctionCall();
  clearSelections();
  state.wordIndex = normalizeIndex(state.wordIndex + 1, state.tokensCount);
  // skip if not a word:
  if (!checkIfWord(state.wordIndex)) {
    state.wordIndex = normalizeIndex(state.wordIndex + 1, state.tokensCount);
    selectWord(state.wordIndex);
    return;
  }

  state.charIndex = 0;
  state.wordIsSelected = true;
  selectWord(state.wordIndex);
  selectChar(state.wordIndex, state.charIndex);
}

function selectWord(wordIndex) {
  logFunctionCall();
  document
    .querySelector(`[data-wd-idx="${wordIndex}"]`)
    .classList.add("selected-word");
}

function getWordDiaCount(wordIndex) {
  logFunctionCall();
  return wd_dict[wordIndex].wordDiaCount;
}

function checkIfWord(wordIndex) {
  logFunctionCall();
  try {
    return wd_dict[wordIndex]["isWord"];
  } catch (error) {
    console.error(`Error checking word at index ${wordIndex}:`, error);
    return false;
  }
}

// ============================
// Character-Level Operations
// ============================
export function charNavigator(state) {
  logFunctionCall();
  if (!state.wordIsSelected) return;
  clearSelections();

  // skip token if it's not a word
  if (!checkIfWord(state.wordIndex)) {
    state.wordIndex = normalizeIndex(state.wordIndex + 1, state.tokensCount);
    selectWord(state.wordIndex);
    return;
  }

  const wordDiaCount = getWordDiaCount(state.wordIndex);
  state.charIndex = normalizeIndex(state.charIndex + 1, wordDiaCount);
  selectChar(state.wordIndex, state.charIndex);
}

function selectChar(wordIndex, charIndex) {
  logFunctionCall();
  if (!checkIfWord(wordIndex)) return;
  const wordElement = document.querySelector(`[data-wd-idx="${wordIndex}"]`);
  wordElement
    .querySelector(`[data-char-idx="${charIndex}"]`)
    .classList.add("selected-char", "blinking-cursor");
}

// ============================
// Diacritic Operations
// ============================
export function addDiaByLocalIndex(state, event) {
  logFunctionCall();
  const { wordIndex, charIndex } = state;
  if (!checkIfWord(wordIndex)) return;

  const wordElement = document.querySelector(`[data-wd-idx="${wordIndex}"]`);
  const diaElement = wordElement.querySelector(`[data-dia-idx="${charIndex}"]`);
  const charElement = wordElement.querySelector(
    `[data-char-idx="${charIndex}"]`
  );

  // If no diaElement or it doesn't have data-dia attribute, skip this position
  if (!diaElement || !diaElement.hasAttribute("data-dia")) {
    // Move to next character
    charNavigator(state);
    return;
  }

  const diaChar = getDiacriticChar(event);
  if (!diaChar) return;

  // Add validation check
  if (!validateDiacritic(diaElement, diaChar)) {
    console.log("Incorrect diacritic");
    return;
  }

  diaElement.innerHTML = diaChar;
  diaElement.classList.add("selected-char", "blinking-cursor");
  charElement.classList.add("selected-char", "blinking-cursor");
  state.currentDia = diaChar;
}

export function addDiaByGlobalIndex(state, event) {
  logFunctionCall();
  const globalDiaIndex = normalizeIndex(
    state.globalDiaIndex,
    state.totalDiacritics
  );

  const diaElement = document.querySelector(
    `[data-global-dia-idx="${globalDiaIndex}"]`
  );
  // If no diaElement or it doesn't have data-dia attribute, move to next position
  if (!diaElement || !diaElement.hasAttribute("data-dia")) {
    state.globalDiaIndex = normalizeIndex(
      globalDiaIndex + 1,
      state.totalDiacritics
    );
    prepareNextDiaPosition(state);
    console.log(`globalIndex: >>> ${state.globalDiaIndex}`);
    return;
  }

  const diaChar = getDiacriticChar(event);
  if (!diaChar) return;

  // Add validation check
  if (!validateDiacritic(diaElement, diaChar)) {
    console.log("Incorrect diacritic");
    return;
  }

  diaElement.innerHTML = diaChar;
  diaElement.classList.add("dia");
  state.currentDia = diaChar;

  // Update global index and selection
  state.globalDiaIndex = normalizeIndex(
    globalDiaIndex + 1,
    state.totalDiacritics
  );
  prepareNextDiaPosition(state);
}

function prepareNextDiaPosition(state) {
  logFunctionCall();
  const charElement = document.querySelector(
    `[data-global-char-idx="${state.globalDiaIndex}"]`
  );
  if (charElement) {
    charElement.classList.add("selected-char", "blinking-cursor");
    selectDiacriticByGlobalIndex(state.globalDiaIndex);
    state.currentChar = charElement.textContent;
  }
}

export function selectDiacriticByGlobalIndex(globalIndex) {
  logFunctionCall();
  clearSelections();
  const charElement = document.querySelector(
    `[data-global-char-idx="${globalIndex}"]`
  );
  if (charElement) {
    charElement.classList.add("selected-char", "blinking-cursor");
  }
}

// In utils.js
function validateDiacritic(element, diacriticChar) {
  // If there's no data-dia attribute, this position shouldn't accept diacritics
  if (!element.hasAttribute("data-dia")) {
    return false; // Return false to move to next character
  }

  const correctDiacritic = element.getAttribute("data-dia");
  return correctDiacritic === diacriticChar;
}

// ============================
// Helper Functions
// ============================
function getDiacriticChar(event) {
  logFunctionCall();
  const key = recreateKey(event);
  return DIACRITICS_CONFIG[key]?.char;
}

function recreateKey(event) {
  logFunctionCall();
  const modifiers = [
    event.ctrlKey && "ctrl",
    event.altKey && "alt",
    event.shiftKey && "shift",
  ]
    .filter(Boolean)
    .join("+");

  const key = event.key === " " ? "space" : `num_${event.key}`;
  return modifiers ? `${modifiers}+${key}` : key;
}

// Event logging utility
export const logEvent = () => {
  logFunctionCall();
  document.addEventListener("keydown", (event) => {
    console.log(`Key pressed: ${event.key}`);
    console.log(event);
  });
};
