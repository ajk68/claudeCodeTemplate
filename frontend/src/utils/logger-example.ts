/**
 * Example usage of the logger utility in TypeScript/JavaScript.
 */

import { Logger, getLogger, info, warning, error } from './logger';

// Method 1: Class-based logger with custom name
const customLogger = new Logger('my-component');
customLogger.info('Component initialized');
customLogger.warning('Props validation failed, using defaults');
customLogger.error('Failed to fetch user data');

// Method 2: Module-level convenience functions
info('App started');
warning('Browser localStorage not available');
error('Network request failed');

// Method 3: Multiple loggers for different modules
const authLogger = new Logger('auth');
const apiLogger = new Logger('api-client');

authLogger.info('User logged in successfully');
apiLogger.info('API request completed in 250ms');

// Method 4: Using getLogger for singleton pattern
const appLogger = getLogger(); // Uses default name
appLogger.info('Application ready');

// Method 5: Component-specific logger
export class UserService {
  private logger = new Logger('UserService');

  async getUser(id: string) {
    this.logger.info(`Fetching user ${id}`);
    try {
      // ... fetch logic
      this.logger.info(`User ${id} loaded successfully`);
    } catch (error) {
      this.logger.error(`Failed to load user ${id}: ${error}`);
    }
  }
}