"""Where the measuring aids write their scratch images and find figrender.

Both default to folders next to the sources (ignored by git) and can be
moved with COURSRADIO_WORK and COURSRADIO_FIGRENDER."""
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WORK_DIR = os.environ.get("COURSRADIO_WORK", os.path.join(ROOT, "build-work"))
# cmake -S tools/figrender -B build-figrender && cmake --build build-figrender
FIGRENDER = os.environ.get("COURSRADIO_FIGRENDER", os.path.join(ROOT, "build-figrender", "figrender"))
