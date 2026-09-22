"""Register broad reference notes without bloating the main build script."""

from cs231n_note import register_cs231n
from prml_note import register_prml


def register_reference_notes(
    note,
    section,
    table,
    callout,
    equation,
    flow,
):
    """Register course- and textbook-level notes."""

    helpers = {
        "note": note,
        "section": section,
        "table": table,
        "callout": callout,
        "equation": equation,
        "flow": flow,
    }
    register_cs231n(**helpers)
    register_prml(**helpers)
