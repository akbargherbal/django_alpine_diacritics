// utils.js
import { ar_alpha, diacritics } from "./data.js";

export const normalizeIndex = (index, maxLen) => {
  if (index >= maxLen) return 0;
  if (index < 0) return maxLen - 1;
  return index;
};

export const wordNavigator = (state) => {
  state.charIndex = -1;
  state.wordIndex = normalizeIndex(state.wordIndex + 1, state.tokensCount);
  state.wordSelected = true;

  clearSelections();
  selectWord(state.wordIndex);
};

export const charNavigator = (state) => {
  clearSelections();
  state.wordIndex = state.wordIndex >= 0 ? state.wordIndex : 0;
  const isWord = checkIfWord(state.wordIndex);

  if (!isWord) {
    state.wordIndex = normalizeIndex(state.wordIndex + 1, state.tokensCount);
    selectWord(state.wordIndex);
    return;
  }

  const wordLen = getWordLength(state.wordIndex);
  state.charIndex = normalizeIndex(state.charIndex + 1, wordLen);

  selectChar(state.wordIndex, state.charIndex);
};

export const handleDiacritics = (event, state) => {
  console.log("handleDiacritics called");
  console.log("Key pressed:", event.key);

  state.currentDia = event.key;
};

const clearSelections = () => {
  document.querySelectorAll("span").forEach((word) => {
    word.classList.remove("selected-word", "selected-char");
  });
};

const selectWord = (wordIndex) => {
  document
    .querySelector(`[data-wd-idx="${wordIndex}"]`)
    .classList.add("selected-word");
};

const selectChar = (wordIndex, charIndex) => {
  const wordElement = document.querySelector(`[data-wd-idx="${wordIndex}"]`);
  console.log(wordElement);
  wordElement
    .querySelector(`[data-char-idx="${charIndex}"]`)
    .classList.add("selected-char");
};

const addDia = (letter, dia) => {
  return letter + dia.join("");
};

// log keyboard:
export const logEvent = () => {
  document.addEventListener("keydown", (event) => {
    const key = event.key;
    console.log(`Key pressed: ${key}`);
    console.log(event); // Changed 'e' to 'event'
  });
};

const getWordLength = (wordIndex) => {
  const wordElement = document.querySelector(`[data-wd-idx="${wordIndex}"]`);
  return parseInt(wordElement.getAttribute("data-wd-len"));
};

const checkIfWord = (wordIndex) => {
  const wordElement = document.querySelector(`[data-wd-idx="${wordIndex}"]`);
  let isWord = wordElement.getAttribute("data-is-word");
  isWord = isWord === "true" ? true : false;
  return isWord;
};
