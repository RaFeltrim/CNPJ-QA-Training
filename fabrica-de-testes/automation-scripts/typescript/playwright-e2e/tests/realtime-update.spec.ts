import { test, expect } from '@playwright/test';
import { DashboardPage } from '../pages/DashboardPage';
import { RealtimePage } from '../pages/RealtimePage';

test('Real-time Updates › should show real-time updates active', async ({ page }) => {
  const dashboard = new DashboardPage(page);
  await dashboard.goto();

  const realtimePage = new RealtimePage(page);
  await realtimePage.validateRealtimeActive();
  await realtimePage.validateDashboardLoaded();
});