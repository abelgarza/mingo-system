import asyncio
import os
from playwright.async_api import async_playwright
from dotenv import load_dotenv

async def run():
    load_dotenv()
    vpn_url = os.environ.get("VPN_URL", "https://vpn.tec.mx")
    
    async with async_playwright() as p:
        # We need a browser to handle the SAML redirect
        browser = await p.chromium.launch(headless=False) # Headless=False so user can see/login if needed
        context = await browser.new_context()
        page = await context.new_page()
        
        print(f"Navigating to {vpn_url}...")
        await page.goto(vpn_url)
        
        print("Waiting for you to log in (if needed)...")
        # In a real tool, we would wait for the URL to change back to the VPN domain
        # or for a specific cookie to appear.
        
        # For diagnostic, let's just wait 60 seconds or until user closes.
        try:
            await page.wait_for_timeout(60000)
        except:
            pass
            
        cookies = await context.cookies()
        print("\nCookies found:")
        for cookie in cookies:
            print(f"{cookie['name']}: {cookie['value'][:10]}...")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
