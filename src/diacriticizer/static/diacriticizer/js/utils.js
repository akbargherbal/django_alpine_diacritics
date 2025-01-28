// utils.js
import { DIACRITICS_CONFIG } from "./data.js";
import { logFunctionCall } from "./logger.js";
// ============================
// Core Navigation Functions
// ============================
function normalizeIndex(index, maxLen) {
  if (index >= maxLen) return 0;
  if (index < 0) return maxLen - 1;
  return index;
}

function clearSelections() {
  document.querySelectorAll("span").forEach((word) => {
    word.classList.remove("selected-word", "selected-char", "blinking-cursor");
  });
}

// ============================
// Word-Level Operations
// ============================
function wordNavigator(state) {
  clearSelections();
  state.wordIndex = normalizeIndex(state.wordIndex + 1, state.tokensCount);
  // skip if to the next word if not a word:
  if (!checkIfWord(state.wordIndex)) {
    wordNavigator(state);
    return;
  }

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

function getWordDiaCount(wordIndex) {
  return wd_dict[wordIndex].wordDiaCount;
}

function checkIfWord(wordIndex) {
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
function charNavigator(state) {
  if (!state.wordIsSelected) return;
  clearSelections();

  const wordDiaCount = getWordDiaCount(state.wordIndex);
  state.charIndex = normalizeIndex(state.charIndex + 1, wordDiaCount);
  selectChar(state.wordIndex, state.charIndex);
  const wordElement = document.querySelector(
    `[data-wd-idx="${state.wordIndex}"]`
  );
  const charElement = wordElement.querySelector(
    `[data-char-idx="${state.charIndex}"]`
  );
  state.globalDiaIndex = parseInt(
    charElement.getAttribute("data-global-char-idx")
  );
  console.log(`Current Global Index: ${state.globalDiaIndex}`);
}

function selectChar(wordIndex, charIndex) {
  if (!checkIfWord(wordIndex)) return;
  const wordElement = document.querySelector(`[data-wd-idx="${wordIndex}"]`);
  wordElement
    .querySelector(`[data-char-idx="${charIndex}"]`)
    .classList.add("selected-char", "blinking-cursor");
}

// ============================
// Diacritic Operations
// ============================
function addDiaByLocalIndex(state, event) {
  const { wordIndex, charIndex } = state;
  if (!checkIfWord(wordIndex)) return;

  const globalCharIndex =
    char_dict_local[`${wordIndex}_${charIndex}`]["global_dia_idx"];
  state.globalDiaIndex = globalCharIndex;
  const diaChar = getDiacriticChar(event);
  if (!diaChar) return;

  // Add validation check
  if (state.mode === "train" && !validateDiacritic(globalCharIndex, diaChar))
    return;

  const wordElement = document.querySelector(`[data-wd-idx="${wordIndex}"]`);
  const diaElement = wordElement.querySelector(`[data-dia-idx="${charIndex}"]`);
  const charElement = wordElement.querySelector(
    `[data-char-idx="${charIndex}"]`
  );
  diaElement.innerHTML = diaChar;
  diaElement.classList.add("selected-char", "blinking-cursor");
  charElement.classList.add("selected-char", "blinking-cursor");
  state.currentDia = diaChar;
}

function addDiaByGlobalIndex(state, event) {
  clearSelections();
  state.globalDiaIndex = normalizeIndex(
    state.globalDiaIndex,
    state.totalDiacritics
  );

  state.wordIndex = char_dict_global[state.globalDiaIndex]["wd_idx"];
  state.charIndex = char_dict_global[state.globalDiaIndex]["local_char_idx"];

  // skip if it has no diacritics.
  if (!char_dict_global[state.globalDiaIndex]["has_dia"]) {
    addDiaByGlobalIndex(state, event);
    return;
  }

  cursor(state.globalDiaIndex, state.totalDiacritics);

  const diaChar = getDiacriticChar(event);
  if (!diaChar) return;

  // Add validation check
  if (
    state.mode === "train" &&
    !validateDiacritic(state.globalDiaIndex, diaChar)
  )
    return;

  const diaElement = document.querySelector(
    `[data-global-dia-idx="${state.globalDiaIndex}"]`
  );
  diaElement.innerHTML = diaChar;
  diaElement.classList.add("dia");
  state.currentDia = diaChar;

  state.globalDiaIndex = state.globalDiaIndex + 1;
  cursor(state.globalDiaIndex, state.totalDiacritics);
}

function validateDiacritic(globalCharIDX, diacriticChar) {
  const correctDiacritic = char_dict_global[globalCharIDX]["dia"];
  return correctDiacritic === diacriticChar;
}

function cursor(index, max_limit) {
  clearSelections();
  const newIndex = normalizeIndex(index, max_limit);
  const charElement = document.querySelector(
    `[data-global-char-idx="${newIndex}"]`
  );
  try {
    charElement.classList.add("selected-char", "blinking-cursor");
  } catch (error) {
    console.error("Error adding cursor:", error);
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

  const key = event.key === " " ? "space" : `num_${event.key}`;
  return modifiers ? `${modifiers}+${key}` : key;
}

export {
  normalizeIndex,
  clearSelections,
  wordNavigator,
  charNavigator,
  addDiaByLocalIndex,
  addDiaByGlobalIndex,
  validateDiacritic,
  getDiacriticChar,
  recreateKey,
};
