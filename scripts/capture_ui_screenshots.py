import asyncio
import os
import subprocess
import time
from playwright.async_api import async_playwright

async def capture_dashboard():
    os.makedirs("reports/assets", exist_ok=True)
    print("Starting FastAPI and Vite servers...")
    
    # Start Backend
    backend_proc = subprocess.Popen(
        ["uvicorn", "backend.app.main:app", "--port", "8000"],
        cwd=os.path.abspath("."),
        shell=True
    )
    
    # Start Frontend
    frontend_proc = subprocess.Popen(
        ["npm.cmd", "run", "dev:frontend"],
        cwd=os.path.abspath("frontend"),
        shell=True
    )
    
    print("Waiting 5 seconds for servers to start...")
    time.sleep(5)
    
    print("Starting Playwright capture...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        
        try:
            print("Navigating to http://localhost:5173...")
            await page.goto("http://localhost:5173", wait_until="networkidle", timeout=30000)
            
            # Give React a moment to render
            await page.wait_for_timeout(2000)
            
            print("Taking initial state screenshot...")
            await page.screenshot(path="reports/assets/ui_dashboard_initial.png", full_page=True)
            
            # Click the "Run Risk Prediction" button
            print("Running risk prediction...")
            await page.click("button[type='submit']")
            # Wait for the result card to appear
            await page.wait_for_selector(".result-card", timeout=5000)
            # Give the animation time to finish
            await page.wait_for_timeout(1000)
            
            print("Taking prediction result screenshot...")
            await page.screenshot(path="reports/assets/ui_dashboard_result.png", full_page=True)
            print("Screenshots captured successfully!")
            
        except Exception as e:
            print(f"Playwright encountered an error: {e}")
            
        finally:
            await browser.close()
            
    # Cleanup servers
    print("Terminating servers...")
    backend_proc.terminate()
    frontend_proc.terminate()
    print("Done!")

if __name__ == "__main__":
    asyncio.run(capture_dashboard())
