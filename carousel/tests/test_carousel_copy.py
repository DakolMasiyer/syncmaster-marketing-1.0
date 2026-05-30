import json
from generators import carousel_copy

POST = {"id": "TEST-01", "type": "Carousel", "pillar": "Education", "persona": "Tunde",
        "platform": "Instagram", "topic": "Sync pay"}
COPY = {"body": "A composer earned $5,000 from one sync.\n\n$5,000 is the market rate.\n\nThe market is real.\n\nApply now.",
        "hook": "A composer earned $5,000 from one sync.", "cta": "Apply at syncmaster.io"}

def test_slides_capped_at_seven(tmp_path):
    out = carousel_copy.generate(POST, COPY, tmp_path)
    data = json.loads(out.read_text())
    assert data["slide_count"] <= 7
    assert data["slides"][0]["archetype"] == "hook"
    assert data["slides"][-1]["archetype"] == "cta"

def test_every_text_field_has_font_size(tmp_path):
    out = carousel_copy.generate(POST, COPY, tmp_path)
    data = json.loads(out.read_text())
    for s in data["slides"]:
        assert "fonts" in s            # {field: font_size}
        for field in ("headline", "body"):
            if s.get(field):
                assert field in s["fonts"]
