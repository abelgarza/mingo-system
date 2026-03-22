"""
Core Scraper using Playwright.
"""

from abc import ABC, abstractmethod
import logging
from playwright.async_api import async_playwright, Page, BrowserContext

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """
    Abstract base class for all Playwright-based web scrapers.
    Handles browser lifecycle and context management.
    """

    def __init__(self, headless: bool = True):
        self.headless = headless

    @abstractmethod
    async def navigate_and_scrape(self, page: Page) -> str | dict:
        """
        Specific navigation and scraping logic.
        Must be implemented by subclasses.
        Should return path to downloaded file, or scraped raw dictionary.
        """
        pass

    async def run(self) -> str | dict:
        """
        Initializes the browser, context, and page, then calls the specific scraping logic.
        """
        async with async_playwright() as p:
            logger.info("Launching Playwright Chromium browser.")
            browser = await p.chromium.launch(headless=self.headless)
            context = await browser.new_context()
            page = await context.new_page()
            
            try:
                result = await self.navigate_and_scrape(page)
                return result
            except Exception as e:
                logger.error(f"Error during scraping process: {str(e)}")
                raise
            finally:
                logger.info("Closing browser.")
                await browser.close()
