import http.server
import socketserver
import threading
import time
import webbrowser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STITCHED_IMAGE = BASE_DIR / "stitched_img.png"
HTML_FILE = BASE_DIR / "panorama_viewer.html"
PORT = 5050

if not STITCHED_IMAGE.exists():
    raise SystemExit(
        "stitched_img.png not found. Run pan_cap.py first or provide a stitched image at the root."
    )

html_content = """<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Street View Panorama</title>
    <link
      rel=\"stylesheet\"
      href=\"https://cdn.jsdelivr.net/npm/pannellum@2.5.6/build/pannellum.css\"
    >
    <style>
      body, html {
        margin: 0;
        height: 100%;
        background: #0b0b0f;
        color: #fff;
        font-family: 'Segoe UI', sans-serif;
      }
      #panorama {
        height: 100vh;
        width: 100vw;
      }
    </style>
  </head>
  <body>
    <div id=\"panorama\"></div>
    <script src=\"https://cdn.jsdelivr.net/npm/pannellum@2.5.6/build/pannellum.js\"></script>
    <script>
      pannellum.viewer('panorama', {
        type: 'equirectangular',
        panorama: 'stitched_img.png',
        autoLoad: true,
        showZoomCtrl: false,
        preview: 'stitched_img.png',
        yaw: 0,
        hfov: 100
      });
    </script>
  </body>
</html>
"""

HTML_FILE.write_text(html_content, encoding="utf-8")

class _Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)


def main() -> None:
    with socketserver.TCPServer(('localhost', PORT), _Handler) as httpd:
        server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        server_thread.start()
        url = f'http://localhost:{PORT}/{HTML_FILE.name}'
        webbrowser.open(url)
        print(f'Hosting panorama at {url} (Ctrl+C to stop)')
        try:
            while server_thread.is_alive():
                time.sleep(0.5)
        except KeyboardInterrupt:
            print('\nStopping panorama server...')
        finally:
            httpd.shutdown()
            httpd.server_close()


if __name__ == '__main__':
    main()