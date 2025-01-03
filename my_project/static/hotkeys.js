// hotkeys.js
import "./node_modules/hotkeys-js/dist/hotkeys.min.js"; // Import the script
import { DIACRITICS_CONFIG } from "./data.js";
const hotkeys = window.hotkeys; // Use the global variable

export function setupHotkeys(appFunctions) {
  // Word and character navigation
  hotkeys("ctrl+space", function (event) {
    event.preventDefault();
    appFunctions.wordNavigator();
  });

  hotkeys("space", function (event) {
    event.preventDefault();
    appFunctions.charNavigator();
  });

  // Set up diacritics hotkeys
  hotkeys("f", function (event) {
    event.preventDefault();
    appFunctions.fatha();
  });

  // Set up diacritics hotkeys
  Object.entries(DIACRITICS_CONFIG).forEach(([key, value]) => {
    hotkeys(key, function (event) {
      event.preventDefault();
      appFunctions.addDia();
    });
  });

  hotkeys("enter,escape", function (event) {
    event.preventDefault();
    appFunctions.toggleEditMode(event);
  });
}
