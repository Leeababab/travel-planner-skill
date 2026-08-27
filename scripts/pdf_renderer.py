import os
import argparse
from playwright.sync_api import sync_playwright

CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def render_techo_pdf_and_pages(html_path, output_pdf_path, output_pages_dir, dpi=300):
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    os.makedirs(output_pages_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=CHROME_PATH if os.path.exists(CHROME_PATH) else None,
            headless=True
        )
        # deviceScaleFactor 2 for crisp 300+ DPI text and badges
        context = browser.new_context(
            viewport={"width": 1240, "height": 1754},
            device_scale_factor=2
        )
        page = context.new_page()

        file_url = f"file://{os.path.abspath(html_path)}"
        page.goto(file_url, wait_until="networkidle")

        # Synchronization guards
        page.evaluate("() => document.fonts.ready")
        page.wait_for_function("() => Array.from(document.images).every(img => img.complete && img.naturalHeight > 0)")
        page.wait_for_timeout(1000)

        # 1. Generate multi-page print PDF
        page.pdf(
            path=output_pdf_path,
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
            margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"}
        )
        print(f"[PDF] Generated: {output_pdf_path} ({os.path.getsize(output_pdf_path)} bytes)")

        # 2. Generate high-res preview PNG for each .page container
        page_elements = page.query_selector_all(".page")
        for idx, elem in enumerate(page_elements):
            png_path = os.path.join(output_pages_dir, f"page_{idx+1}.png")
            elem.screenshot(path=png_path)
            print(f"[Page {idx+1}] Saved: {png_path}")

        browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deterministic Playwright PDF & PNG Renderer")
    parser.add_argument("--html", required=True, help="Path to input HTML template")
    parser.add_argument("--pdf", required=True, help="Path to output PDF")
    parser.add_argument("--pages-dir", required=True, help="Directory for page preview PNGs")
    args = parser.parse_args()

    render_techo_pdf_and_pages(args.html, args.pdf, args.pages_dir)
