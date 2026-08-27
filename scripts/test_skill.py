import os
import sys
import unittest
import yaml
import json
import jsonschema

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(SCRIPT_DIR, "..")
FIXTURE_PATH = os.path.join(ROOT_DIR, "tests", "fixtures", "sample_trip.yaml")
SCHEMA_PATH = os.path.join(ROOT_DIR, "schemas", "trip_spec.schema.json")

class TestTravelPlannerSkill(unittest.TestCase):

    def test_schema_validity(self):
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            schema = json.load(f)
        jsonschema.Draft202012Validator.check_schema(schema)
        self.assertTrue(True, "Schema is valid Draft202012")

    def test_sample_trip_conformance(self):
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            schema = json.load(f)
        with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        jsonschema.validate(data, schema)
        self.assertEqual(data["trip_id"], "tokyo_sample_2026")

    def test_build_trip_compilation(self):
        from build_trip import build_trip
        out_dir = os.path.join(ROOT_DIR, "output", "test_run")
        build_trip(FIXTURE_PATH, out_dir)

        pdf_path = os.path.join(out_dir, "tokyo_sample_2026_Travel_Journal.pdf")
        map_path = os.path.join(out_dir, "interactive_travel_map.html")
        page1_path = os.path.join(out_dir, "pages", "page_1.png")

        self.assertTrue(os.path.exists(pdf_path), "PDF exists")
        self.assertGreater(os.path.getsize(pdf_path), 50000, "PDF is non-empty")
        self.assertTrue(os.path.exists(map_path), "Interactive map exists")
        self.assertTrue(os.path.exists(page1_path), "Page 1 PNG exists")

if __name__ == "__main__":
    unittest.main()
