# 🧭 Travel Planner & Zakka Techo System (Antigravity Skill)

A production-grade, reusable **Antigravity Skill** for end-to-end travel planning, publication-grade Japanese Zakka Techo (A4 PDF) generation, and interactive Leaflet Triple-View web application compilation.

---

## 🌟 Key Features

1. **Structured Data & Schema Decoupling**:
   - Clean separation of trip data (`trip_spec.yaml` conforming to `trip_spec.schema.json`) from visual presentation.
2. **Japanese Zakka-Styled Techo Generator (出版級手帳)**:
   - Dot-grid paper background, washi tapes, Caveat cursive typography, Zen Maru Gothic headers, stamp boxes, food & hotel spotlights, and expense tracking.
   - Deterministic Headless Playwright PDF rendering with font synchronization and image complete validation.
3. **Leaflet Triple-View Interactive SPA**:
   - Switcher between `🗺️ Interactive Map`, `📖 In-Browser Journal Reader`, and `📑 Split Mode`.
   - Day-by-day polyline highway tracking, deep Google Maps links, and floating quick-zoom buttons.
4. **Google Cloud Run Deployment Automation**:
   - Zero-config Docker & Nginx multi-service hosting in regional low-latency clusters (`asia-east2`).

---

## 🚀 Quick Start

### Installation into Antigravity
```bash
git clone https://github.com/Leeababab/travel-planner-skill.git
cd travel-planner-skill
./install.sh --link
```

### Build a Trip Package
```bash
python3 scripts/build_trip.py --spec tests/fixtures/sample_trip.yaml --out-dir output/my_trip
```

### Run Self-Test Suite
```bash
python3 scripts/test_skill.py
```
