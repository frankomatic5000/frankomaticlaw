import { readFile, writeFile } from 'fs/promises';
import { join } from 'path';
import crypto from 'crypto';

interface StoredToken {
  accessToken: string;
  refreshToken?: string;
  expiresAt?: number;
  scopes: string[];
}

export class TokenManager {
  private tokenPath: string;
  private storeDomain: string;

  constructor(storeDomain: string) {
    this.storeDomain = storeDomain;
    this.tokenPath = join(
      process.env.HOME || process.env.USERPROFILE || '',
      '.openclaw',
      'credentials',
      'shopify',
      `${this.sanitizeDomain(storeDomain)}.json`
    );
  }

  private sanitizeDomain(domain: string): string {
    return domain.replace(/[^a-zA-Z0-9]/g, '_');
  }

  async getToken(): Promise<StoredToken | null> {
    try {
      const data = await readFile(this.tokenPath, 'utf-8');
      const encrypted = JSON.parse(data);
      return this.decrypt(encrypted);
    } catch {
      return null;
    }
  }

  async saveToken(token: StoredToken): Promise<void> {
    const encrypted = this.encrypt(token);
    await writeFile(this.tokenPath, JSON.stringify(encrypted, null, 2));
  }

  async refreshToken(): Promise<string | null> {
    const token = await this.getToken();
    if (!token?.refreshToken) {
      return null;
    }

    // In real implementation, this would call Shopify OAuth refresh endpoint
    // For now, return existing token
    return token.accessToken;
  }

  private encrypt(data: StoredToken): any {
    // Simple encryption using environment key
    const key = process.env.OPENCLAW_ENCRYPTION_KEY || 'default-key-32-chars-long!!!!!'; // Must be 32 chars
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv('aes-256-cbc', Buffer.from(key), iv);
    
    const jsonData = JSON.stringify(data);
    let encrypted = cipher.update(jsonData, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    
    return {
      iv: iv.toString('hex'),
      data: encrypted,
    };
  }

  private decrypt(encrypted: any): StoredToken {
    const key = process.env.OPENCLAW_ENCRYPTION_KEY || 'default-key-32-chars-long!!!!!';
    const iv = Buffer.from(encrypted.iv, 'hex');
    const decipher = crypto.createDecipheriv('aes-256-cbc', Buffer.from(key), iv);
    
    let decrypted = decipher.update(encrypted.data, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    
    return JSON.parse(decrypted);
  }
}
