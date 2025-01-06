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

export function logFunctionCall() {
  const error = new Error();
  const stack = error.stack.split('\n');
  const functionNameMatch = stack[2].match(/at (.+?) \(/);
  const functionName = functionNameMatch ? functionNameMatch[1] : 'anonymous function';
  console.log(`Calling from ${functionName}`);
}
