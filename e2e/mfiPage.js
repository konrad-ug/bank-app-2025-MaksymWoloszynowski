import { expect } from "@playwright/test";

export class MFIPage {
  constructor(page) {
    this.page = page;
    this.workersLink = page
      .getByLabel("Nagłówek")
      .getByRole("link", { name: "Pracownicy" });
    this.personnel = page
      .locator(".views-element-container")
      .getByRole("link", { name: "Skład osobowy" });
  }

  async goto() {
    await this.page.goto("https://mfi.ug.edu.pl/");
  }

  async workers() {
    await this.workersLink.click();
    await this.personnel.click();
  }

  async searchWorker(search, expected) {
    await this.page.getByLabel("Imię lub nazwisko").fill(search);

    await expect(this.page.getByRole("link", { name: expected })).toBeVisible();

    await this.page.getByRole("link", { name: expected }).click();
  }
}
