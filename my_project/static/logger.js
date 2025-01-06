// logger.js
export const Logger = {
    stackTrace: true,
    timing: true,
    
    log(functionName, args = {}, module = 'unknown') {
        const timestamp = new Date().toISOString();
        const stack = new Error().stack;
        
        const logData = {
            timestamp,
            module,
            function: functionName,
            arguments: args
        };
        
        if (this.stackTrace) {
            logData.stack = stack;
        }
        
        if (this.timing) {
            logData.executionTime = performance.now();
        }
        
        console.log(JSON.stringify(logData, null, 2));
    }
};

// Usage example:
// Import in your modules:
// import { Logger } from './logger.js';
// 
// Then in your functions:
// Logger.log('wordNavigator', { wordIndex: this.wordIndex }, 'utils.js');