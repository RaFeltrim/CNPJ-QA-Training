import { test, expect } from '@playwright/test';
import { DashboardPage } from '../pages/DashboardPage';
import { ExportPage } from '../pages/ExportPage';

test('Export Functionality › should export report successfully', async ({ page }) => {
  const dashboard = new DashboardPage(page);
  await dashboard.goto();

  const exportPage = new ExportPage(page);
  await exportPage.clickExportButton();
  await exportPage.validateSuccess();
});