import { Page, expect } from '@playwright/test';

export class RealtimePage {
  constructor(private page: Page) {}

  async validateRealtimeActive() {
    // Texto exato que vemos no print (badge verde)
    const realtimeIndicator = this.page.getByText('Real-time updates active');
    await expect(realtimeIndicator).toBeVisible();
  }

  async validateDashboardLoaded() {
    // Se o dashboard carregou, os cards de métrica existem
    const totalTestsCard = this.page.getByText('Total Tests').first();
    await expect(totalTestsCard).toBeVisible();
  }
}