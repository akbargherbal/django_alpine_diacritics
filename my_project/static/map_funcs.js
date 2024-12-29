// Define your shortcuts map
const shortcuts = {
    'ctrl+p': function() { /* print logic */ },
    'shift+/': function() { /* show shortcuts */ },
    'alt+s': function() { /* save changes */ }
};

// In your Alpine component
{
    shortcuts,
    handleKeyPress(event) {
        const key = [
            event.ctrlKey ? 'ctrl+' : '',
            event.shiftKey ? 'shift+' : '',
            event.altKey ? 'alt+' : '',
            event.key.toLowerCase()
        ].join('');

        if (this.shortcuts[key]) {
            event.preventDefault();
            this.shortcuts[key]();
        }
    }
}