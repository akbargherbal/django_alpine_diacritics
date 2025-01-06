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
    word.classList.remove("selected-word", "selected-char");
  });
}

// ============================
// Word-Level Operations
// ============================
export function wordNavigator(state) {
  logFunctionCall();
  clearSelections();
  state.wordIndex = normalizeIndex(state.wordIndex + 1, state.tokensCount);
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

function getWordLength(wordIndex) {
  logFunctionCall();
  const wordElement = document.querySelector(`[data-wd-idx="${wordIndex}"]`);
  return parseInt(wordElement.getAttribute("data-wd-len"));
}

function checkIfWord(wordIndex) {
  logFunctionCall();
  try {
    const wordElement = document.querySelector(`[data-wd-idx="${wordIndex}"]`);
    let isWord = wordElement.getAttribute("data-is-word");
    return isWord === "true";
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

  if (!checkIfWord(state.wordIndex)) {
    state.wordIndex = normalizeIndex(state.wordIndex + 1, state.tokensCount);
    selectWord(state.wordIndex);
    return;
  }

  const wordLen = getWordLength(state.wordIndex);
  state.charIndex = normalizeIndex(state.charIndex + 1, wordLen);
  selectChar(state.wordIndex, state.charIndex);
}

function selectChar(wordIndex, charIndex) {
  logFunctionCall();
  if (!checkIfWord(wordIndex)) return;
  const wordElement = document.querySelector(`[data-wd-idx="${wordIndex}"]`);
  wordElement
    .querySelector(`[data-char-idx="${charIndex}"]`)
    .classList.add("selected-char");
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

  const diaChar = getDiacriticChar(event);
  if (!diaChar) return;

  diaElement.innerHTML = diaChar;
  diaElement.classList.add("selected-char");
  charElement.classList.add("selected-char");
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

  if (!diaElement) return;

  const diaChar = getDiacriticChar(event);
  if (!diaChar) return;

  diaElement.innerHTML = diaChar;
  diaElement.classList.add("dia");
  state.currentDia = diaChar;

  // Update global index and selection
  state.globalDiaIndex = normalizeIndex(
    globalDiaIndex + 1,
    state.totalDiacritics
  );
  updateGlobalSelection(state);
}

function updateGlobalSelection(state) {
  logFunctionCall();
  const charElement = document.querySelector(
    `[data-global-char-idx="${state.globalDiaIndex}"]`
  );
  if (charElement) {
    charElement.classList.add("selected-char");
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
    charElement.classList.add("selected-char");
  }
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
