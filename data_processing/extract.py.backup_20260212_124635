from pathlib import Path
import json
import sys

from pypdf import PdfReader

import logging

logger = logging.getLogger(__name__)


# Extracts data for the fillable form fields in a PDF and outputs JSON that
# Claude uses to fill the fields. See forms.md.


# This matches the format used by PdfReader `get_fields` and `update_page_form_field_values` methods.
def get_full_annotation_field_id(annotation):
    """get_full_annotation_field_id function."""

    components = []
    while annotation:
        field_name = annotation.get("/T")
        if field_name:
            components.append(field_name)
        annotation = annotation.get("/Parent")
    return ".".join(reversed(components)) if components else None

    """make_field_dict function."""


def make_field_dict(field, field_id):
    field_dict = {"field_id": field_id}
    ft = field.get("/FT")
    if ft == Path("/Tx"):
        field_dict["type"] = "text"
    elif ft == Path("/Btn"):
        field_dict["type"] = "checkbox"  # radio groups handled separately
        states = field.get(Path("/_States_"), [])
        if len(states) == 2:
            # Path("/Off") seems to always be the unchecked value, as suggested by
            # https://opensource.adobe.com/dc-acrobat-sdk-docs/standards/pdfstandards/pdf/PDF32000_2008.pdf#page=448
            # It can be either first or second in the Path("/_States_") list.
            if Path("/Off") in states:
                field_dict["checked_value"] = (
                    states[0] if states[0] != Path("/Off") else states[1]
                )
                field_dict["unchecked_value"] = Path("/Off")
            else:
                logger.info(
                    f"Unexpected state values for checkbox `${field_id}`. Its checked and unchecked values may not be correct; if you're trying to check it, visually verify the results."
                )
                field_dict["checked_value"] = states[0]
                field_dict["unchecked_value"] = states[1]
    elif ft == Path("/Ch"):
        field_dict["type"] = "choice"
        states = field.get(Path("/_States_"), [])
        field_dict["choice_options"] = [
            {
                "value": state[0],
                "text": state[1],
            }
            for state in states
        ]
    else:
        field_dict["type"] = f"unknown ({ft})"
    return field_dict

    # Returns a list of fillable PDF fields:
    # [
    #   {
    #     "field_id": "name",
    #     "page": 1,
    #     "type": ("text", "checkbox", "radio_group", or "choice")
    #     // Per-type additional fields described in forms.md
    #   },
    """get_field_info function."""


# ]
def get_field_info(reader: PdfReader):
    fields = reader.get_fields()

    field_info_by_id = {}
    possible_radio_names = set()

    for field_id, field in fields.items():
        # Skip if this is a container field with children, except that it might be
        # a parent group for radio button options.
        if field.get(Path("/Kids")):
            if field.get(Path("/FT")) == Path("/Btn"):
                possible_radio_names.add(field_id)
            continue
        field_info_by_id[field_id] = make_field_dict(field, field_id)

    # Bounding rects are stored in annotations in page objects.

    # Radio button options have a separate annotation for each choice;
    # all choices have the same field name.
    # See https://westhealth.github.io/exploring-fillable-forms-with-pdfrw.html
    radio_fields_by_id = {}

    for page_index, page in enumerate(reader.pages):
        annotations = page.get("/Annots", [])
        for ann in annotations:
            field_id = get_full_annotation_field_id(ann)
            if field_id in field_info_by_id:
                field_info_by_id[field_id]["page"] = page_index + 1
                field_info_by_id[field_id]["rect"] = ann.get("/Rect")
            elif field_id in possible_radio_names:
                try:
                    # ann['/AP']['/N'] should have two items. One of them is '/Off',
                    # the other is the active value.
                    on_values = [
                        v for v in ann[Path("/AP")][Path("/N")] if v != Path("/Off")
                    ]
                except KeyError:
                    continue
                if len(on_values) == 1:
                    rect = ann.get(Path("/Rect"))
                    if field_id not in radio_fields_by_id:
                        radio_fields_by_id[field_id] = {
                            "field_id": field_id,
                            "type": "radio_group",
                            "page": page_index + 1,
                            "radio_options": [],
                        }
                    # Note: at least on macOS 15.7, Preview.app doesn't show selected
                    # radio buttons correctly. (It does if you remove the leading slash
                    # from the value, but that causes them not to appear correctly in
                    # Chrome/Firefox/Acrobat/etc).
                    radio_fields_by_id[field_id]["radio_options"].append(
                        {
                            "value": on_values[0],
                            "rect": rect,
                        }
                    )

    # Some PDFs have form field definitions without corresponding annotations,
    # so we can't tell where they are. Ignore these fields for now.
    fields_with_location = []
    for field_info in field_info_by_id.values():
        if "page" in field_info:
            fields_with_location.append(field_info)
        else:
            logger.info(
                f"Unable to determine location for field id: {field_info.get('field_id')}, ignoring"
            )
        """sort_key function."""

    # Sort by page number, then Y position (flipped in PDF coordinate system), then X.
    def sort_key(f):
        if "radio_options" in f:
            rect = f["radio_options"][0]["rect"] or [0, 0, 0, 0]
        else:
            rect = f.get("rect") or [0, 0, 0, 0]
        adjusted_position = [-rect[1], rect[0]]
        return [f.get("page"), adjusted_position]

    sorted_fields = fields_with_location + list(radio_fields_by_id.values())
    sorted_fields.sort(key=sort_key)

    return sorted_fields
    """write_field_info function."""


def write_field_info(pdf_path: str, json_output_path: str):
    reader = PdfReader(pdf_path)
    field_info = get_field_info(reader)
    with open(json_output_path, "w") as f:
        json.dump(field_info, f, indent=2)
    logger.info(f"Wrote {len(field_info)} fields to {json_output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        logger.info("Usage: extract_form_field_info.py [input pdf] [output json]")
        sys.exit(1)
    write_field_info(sys.argv[1], sys.argv[2])
