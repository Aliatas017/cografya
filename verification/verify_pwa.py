import http.server
import socketserver
import threading
import time
import os
from playwright.sync_api import sync_playwright

# Start a simple HTTP server
PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

# Run the server in a separate thread
thread = threading.Thread(target=start_server)
thread.daemon = True
thread.start()

# Give the server a moment to start
time.sleep(2)

def verify_pwa_tags():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"http://localhost:{PORT}/index.html")

        # Check for manifest link
        manifest_link = page.locator('link[rel="manifest"]')
        if manifest_link.count() > 0:
            print("PASS: Manifest link found.")
            href = manifest_link.get_attribute("href")
            print(f"Manifest href: {href}")
        else:
            print("FAIL: Manifest link NOT found.")

        # Check for theme-color meta tag
        theme_color = page.locator('meta[name="theme-color"]')
        if theme_color.count() > 0:
            print("PASS: Theme-color meta tag found.")
            content = theme_color.get_attribute("content")
            print(f"Theme color: {content}")
        else:
            print("FAIL: Theme-color meta tag NOT found.")

        # Check for Service Worker registration script
        # This is harder to check directly via locator as it's a script tag content,
        # but we can check if the file sw.js is requested or check page content.
        content = page.content()
        if "serviceWorker.register" in content:
             print("PASS: Service Worker registration script found in HTML.")
        else:
             print("FAIL: Service Worker registration script NOT found.")

        # Verify accessibility of manifest.json
        response = page.request.get(f"http://localhost:{PORT}/manifest.json")
        if response.ok:
            print("PASS: manifest.json is accessible.")
            try:
                json_data = response.json()
                print(f"Manifest name: {json_data.get('name')}")
            except:
                print("FAIL: manifest.json is not valid JSON.")
        else:
            print(f"FAIL: manifest.json not accessible. Status: {response.status}")

        # Verify accessibility of sw.js
        response_sw = page.request.get(f"http://localhost:{PORT}/sw.js")
        if response_sw.ok:
            print("PASS: sw.js is accessible.")
        else:
            print(f"FAIL: sw.js not accessible. Status: {response_sw.status}")

        # Take a screenshot
        page.screenshot(path="verification/pwa_verification.png")
        print("Screenshot saved to verification/pwa_verification.png")

        browser.close()

if __name__ == "__main__":
    verify_pwa_tags()
