/**
 * Simple logging utility for writing to centralized logs directory.
 * Zero-dependency logger that integrates with vite-console-forward-plugin.
 */

type LogLevel = 'INFO' | 'WARNING' | 'ERROR';

class Logger {
  private name: string;

  constructor(name?: string) {
    // Default to using the current file/module name or 'unknown'
    this.name = name || this.getDefaultName();
  }

  private getDefaultName(): string {
    // Try to extract name from stack trace or use default
    try {
      const error = new Error();
      const stack = error.stack?.split('\n')[3];
      const match = stack?.match(/\/([^/]+)\.[jt]s/);
      return match?.[1] || 'unknown';
    } catch {
      return 'unknown';
    }
  }

  private writeLog(level: LogLevel, message: string): void {
    // Create ISO timestamp with Z suffix
    const timestamp = new Date().toISOString();
    const logEntry = `[${timestamp}] [${level}] [${this.name}] ${message}`;

    // Write to console (will be captured by vite-console-forward-plugin)
    switch (level) {
      case 'INFO':
        console.log(logEntry);
        break;
      case 'WARNING':
        console.warn(logEntry);
        break;
      case 'ERROR':
        console.error(logEntry);
        break;
    }
  }

  info(message: string): void {
    this.writeLog('INFO', message);
  }

  warning(message: string): void {
    this.writeLog('WARNING', message);
  }

  error(message: string): void {
    this.writeLog('ERROR', message);
  }
}

// Module-level singleton instance
let defaultLogger: Logger | null = null;

/**
 * Get or create a logger instance.
 */
export function getLogger(name?: string): Logger {
  if (name) {
    return new Logger(name);
  }
  if (!defaultLogger) {
    defaultLogger = new Logger();
  }
  return defaultLogger;
}

/**
 * Log info message using default logger.
 */
export function info(message: string): void {
  getLogger().info(message);
}

/**
 * Log warning message using default logger.
 */
export function warning(message: string): void {
  getLogger().warning(message);
}

/**
 * Log error message using default logger.
 */
export function error(message: string): void {
  getLogger().error(message);
}

// Export the Logger class for custom instances
export { Logger };

// Example usage in development
if (import.meta.env.DEV) {
  const testLogger = new Logger('logger-test');
  testLogger.info('Logger utility loaded');
}