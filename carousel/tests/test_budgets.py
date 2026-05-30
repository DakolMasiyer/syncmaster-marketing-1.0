import json
from pathlib import Path

BUDGETS = json.loads((Path(__file__).resolve().parent.parent / "slot_budgets.json").read_text())

def test_carousel_archetypes_present():
    arch = BUDGETS["carousel"]
    assert set(arch) >= {"hook", "context", "showcase", "proof", "cta"}

def test_every_slot_has_required_keys():
    required = {"layer", "kind", "max_lines", "max_chars", "font_max", "font_min"}
    for archetype, slots in BUDGETS["carousel"].items():
        for slot_name, spec in slots.items():
            assert required <= set(spec), f"{archetype}.{slot_name} missing {required - set(spec)}"
            assert spec["font_min"] <= spec["font_max"]
            assert spec["kind"] in ("text", "number")

def test_hook_headline_budget_matches_measurement():
    h = BUDGETS["carousel"]["hook"]["headline"]
    assert h["layer"] == "headline"
    assert h["font_max"] == 320
    assert h["max_lines"] == 3
