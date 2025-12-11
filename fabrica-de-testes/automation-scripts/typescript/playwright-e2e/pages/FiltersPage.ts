import { Page, expect } from '@playwright/test';

export class FiltersPage {
  constructor(private page: Page) {}

  async validateFiltersVisible() {
    // Os filtros existem: vemos "All Time", "dd/mm/yyyy", dropdowns, etc
    const filterSection = this.page.locator('text=Filters').first();
    await expect(filterSection).toBeVisible();
  }

  async validateTableExists() {
    // A tabela "Histórico de Execuções" existe e tem dados
    const table = this.page.locator('table').first();
    await expect(table).toBeVisible();

    // Verifica que tem pelo menos uma linha
    const rows = this.page.locator('table tbody tr');
    await expect(rows.first()).toBeVisible();
  }
}