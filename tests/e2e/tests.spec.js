import { test, expect } from "@playwright/test";
import { MFIPage } from "./mfiPage";

test("Konrad ma pokój 3.10", async ({ page }) => {
    const mfiPlayright = new MFIPage(page)

    await mfiPlayright.goto()
    await mfiPlayright.workers()

    await mfiPlayright.searchWorker('sołtys', 'mgr Konrad Sołtys')

    await expect(page.getByText("Nr pokoju: 4.19")).toBeVisible();
});

test("Anna Baran w IFD", async ({ page }) => {
    const mfiPlayright = new MFIPage(page)

    await mfiPlayright.goto()
    await mfiPlayright.workers()

    await mfiPlayright.searchWorker('baran', 'mgr Anna Baran')

    await expect(page.getByText("Instytut Fizyki Doświadczalnej")).toBeVisible();
});
