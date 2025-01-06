// utils.js
import { DIACRITICS_CONFIG } from "./data.js";

// ============================
// Core Navigation Functions
// ============================
export function normalizeIndex(index, maxLen) {
  if (index >= maxLen) return 0;
  if (index < 0) return maxLen - 1;
  return index;
}

export function clearSelections() {
  document.querySelectorAll("span").forEach((word) => {
    word.classList.remove("selected-word", "selected-char");
  });
}

// ============================
// Word-Level Operations
// ============================
export function wordNavigator(state) {
  clearSelections();
  state.wordIndex = normalizeIndex(state.wordIndex + 1, state.tokensCount);
  state.charIndex = 0;
  state.wordIsSelected = true;
  selectWord(state.wordIndex);
  selectChar(state.wordIndex, state.charIndex);
}

function selectWord(wordIndex) {
  document
    .querySelector(`[data-wd-idx="${wordIndex}"]`)
    .classList.add("selected-word");
}

function getWordLength(wordIndex) {
  const wordElement = document.querySelector(`[data-wd-idx="${wordIndex}"]`);
  return parseInt(wordElement.getAttribute("data-wd-len"));
}

function checkIfWord(wordIndex) {
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
  const key = recreateKey(event);
  return DIACRITICS_CONFIG[key]?.char;
}

function recreateKey(event) {
  const modifiers = [
    event.ctrlKey && "ctrl",
    event.altKey && "alt",
    event.shiftKey && "shift",
  ]
    .filter(Boolean)
    .join("+");

  const num = event.key === " " ? "space" : `num_${event.key}`;
  return modifiers ? `${modifiers}+${num}` : num;
}

// Event logging utility
export const logEvent = () => {
  document.addEventListener("keydown", (event) => {
    console.log(`Key pressed: ${event.key}`);
    console.log(event);
  });
};
