import { Page, expect } from '@playwright/test';

export class ExportPage {
  constructor(private page: Page) {}

  async clickExportButton() {
    // Botão que sabemos que existe (verde no print)
    const exportBtn = this.page.getByText('Export Report');
    await expect(exportBtn).toBeVisible();
    await exportBtn.click();
  }

  async validateSuccess() {
    // Simples: verifica que não quebrou
    await this.page.waitForTimeout(2000);
    await expect(this.page.getByText('Export Report')).toBeEnabled();
  }
}