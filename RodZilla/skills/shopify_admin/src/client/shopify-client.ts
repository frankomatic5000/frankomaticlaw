import { GraphQLClient, RequestOptions } from 'graphql-request';
import { TokenManager } from './auth/token-manager.js';
import { RateLimiter } from './utils/rate-limiter.js';
import { RetryHandler } from './utils/retry-handler.js';

export interface ShopifyConfig {
  storeDomain: string;
  accessToken: string;
  apiVersion?: string;
}

export class ShopifyClient {
  private client: GraphQLClient;
  private rateLimiter: RateLimiter;
  private retryHandler: RetryHandler;
  private tokenManager: TokenManager;

  constructor(private config: ShopifyConfig) {
    const endpoint = `https://${config.storeDomain}/admin/api/${config.apiVersion || '2024-01'}/graphql.json`;
    
    this.client = new GraphQLClient(endpoint, {
      headers: {
        'X-Shopify-Access-Token': config.accessToken,
        'Content-Type': 'application/json',
      },
    });

    this.rateLimiter = new RateLimiter(50); // Shopify GraphQL cost limit
    this.retryHandler = new RetryHandler({
      maxRetries: 3,
      baseDelay: 1000,
      maxDelay: 30000,
    });
    this.tokenManager = new TokenManager(config.storeDomain);
  }

  async execute<T = any>(
    query: string,
    variables?: Record<string, any>,
    options?: RequestOptions
  ): Promise<T> {
    // Check rate limit
    await this.rateLimiter.acquirePermission();

    // Execute with retry logic
    return this.retryHandler.execute(async () => {
      try {
        const result = await this.client.request<T>(query, variables, options);
        
        // Extract cost from response headers if available
        // Shopify returns cost in extensions
        return result;
      } catch (error: any) {
        // Handle specific Shopify errors
        if (error.response?.status === 429) {
          // Rate limited - will retry
          throw new Error('RATE_LIMITED');
        }
        if (error.response?.status === 401) {
          // Auth error - try refresh
          await this.tokenManager.refreshToken();
          throw new Error('AUTH_REFRESH_NEEDED');
        }
        throw error;
      }
    });
  }

  async query<T = any>(
    query: string,
    variables?: Record<string, any>
  ): Promise<T> {
    return this.execute<T>(query, variables);
  }

  async mutate<T = any>(
    mutation: string,
    variables?: Record<string, any>
  ): Promise<T> {
    return this.execute<T>(mutation, variables);
  }

  getStoreDomain(): string {
    return this.config.storeDomain;
  }
}
