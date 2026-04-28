export class RateLimiter {
  private points: number = 50;
  private lastRefill: number = Date.now();
  private readonly maxPoints: number;
  private readonly refillRate: number; // points per second

  constructor(maxPoints: number = 50, refillRate: number = 50) {
    this.maxPoints = maxPoints;
    this.refillRate = refillRate;
  }

  async acquirePermission(cost: number = 1): Promise<void> {
    this.refillPoints();
    
    while (this.points < cost) {
      const waitTime = Math.ceil((cost - this.points) / this.refillRate * 1000);
      await this.delay(waitTime);
      this.refillPoints();
    }
    
    this.points -= cost;
  }

  private refillPoints(): void {
    const now = Date.now();
    const elapsed = (now - this.lastRefill) / 1000; // seconds
    const pointsToAdd = elapsed * this.refillRate;
    
    this.points = Math.min(this.maxPoints, this.points + pointsToAdd);
    this.lastRefill = now;
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  getAvailablePoints(): number {
    this.refillPoints();
    return this.points;
  }
}
