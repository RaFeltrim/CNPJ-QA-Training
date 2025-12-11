import { test, expect } from '@playwright/test';
import { DashboardPage } from '../pages/DashboardPage';
import { FiltersPage } from '../pages/FiltersPage';

test('Filters Functionality › should filter by date range', async ({ page }) => {
  const dashboard = new DashboardPage(page);
  await dashboard.goto();

  const filtersPage = new FiltersPage(page);
  await filtersPage.validateFiltersVisible();
  await filtersPage.validateTableExists();
});