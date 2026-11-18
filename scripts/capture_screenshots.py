import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    os.makedirs('screenshots', exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('http://localhost:8081')
        await page.screenshot(path='screenshots/home.png', full_page=True)
        await browser.close()

asyncio.run(main())
