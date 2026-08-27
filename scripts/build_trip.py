import os
import sys
import json
import yaml
import argparse
from jinja2 import Environment, FileSystemLoader

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(SCRIPT_DIR, "..", "templates")
from pdf_renderer import render_techo_pdf_and_pages

def build_trip(spec_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    pages_dir = os.path.join(output_dir, "pages")
    os.makedirs(pages_dir, exist_ok=True)

    with open(spec_path, "r", encoding="utf-8") as f:
        if spec_path.endswith(".yaml") or spec_path.endswith(".yml"):
            trip_data = yaml.safe_load(f)
        else:
            trip_data = json.load(f)

    trip_id = trip_data.get("trip_id", "trip")
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), autoescape=False)

    # 1. Compile Techo HTML
    techo_template = env.get_template("techo_template.html.j2")
    techo_html = techo_template.render(trip=trip_data)
    techo_html_path = os.path.join(output_dir, f"{trip_id}_techo.html")
    with open(techo_html_path, "w", encoding="utf-8") as f:
        f.write(techo_html)
    print(f"[Build] Techo HTML compiled: {techo_html_path}")

    # 2. Render PDF and Preview Pages via Playwright
    pdf_path = os.path.join(output_dir, f"{trip_id}_Travel_Journal.pdf")
    render_techo_pdf_and_pages(techo_html_path, pdf_path, pages_dir)

    # 3. Extract Spots & Routes for Interactive Map
    all_spots = []
    routes_dict = {
        "all": {
            "title": f"{trip_data.get('title')} 全域總覽",
            "badge": f"{trip_data.get('dates', {}).get('total_days', 1)} 天行程",
            "desc": trip_data.get("subtitle", ""),
            "color": "#0f766e",
            "coords": []
        }
    }

    all_coords = []
    spot_counter = 1
    for day in trip_data.get("days", []):
        day_key = f"d{day.get('day_number', 1)}"
        day_coords = day.get("route_polyline", [])
        routes_dict[day_key] = {
            "title": f"DAY {day.get('day_number')}: {day.get('title')}",
            "badge": day.get("driving_info", ""),
            "desc": day.get("summary", ""),
            "color": "#0284c7" if day.get("day_number", 1) % 2 == 0 else "#0f766e",
            "coords": day_coords
        }
        all_coords.extend(day_coords)

        for s in day.get("spots", []):
            s_copy = dict(s)
            s_copy["day"] = day_key
            s_copy["day_number"] = day.get("day_number")
            if not s_copy.get("id"):
                s_copy["id"] = str(spot_counter)
            all_spots.append(s_copy)
            spot_counter += 1

    routes_dict["all"]["coords"] = all_coords

    # 4. Compile Interactive Map HTML
    map_template = env.get_template("interactive_map.html.j2")
    map_html = map_template.render(
        trip=trip_data,
        spots_json=json.dumps(all_spots, ensure_ascii=False),
        routes_json=json.dumps(routes_dict, ensure_ascii=False)
    )
    map_html_path = os.path.join(output_dir, "interactive_travel_map.html")
    index_html_path = os.path.join(output_dir, "index.html")
    with open(map_html_path, "w", encoding="utf-8") as f:
        f.write(map_html)
    with open(index_html_path, "w", encoding="utf-8") as f:
        f.write(map_html)
    print(f"[Build] Interactive Map SPA compiled: {map_html_path}")

    print(f"🎉 Trip build successfully completed at {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build complete Techo PDF and Interactive Map from YAML/JSON spec.")
    parser.add_argument("--spec", required=True, help="Path to trip_spec YAML/JSON")
    parser.add_argument("--out-dir", required=True, help="Output directory")
    args = parser.parse_args()

    build_trip(args.spec, args.out_dir)
