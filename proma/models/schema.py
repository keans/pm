from dateutil.parser import parse as dateutil_parse
from pytimeparse import parse as pytimeparse_parse


def is_duration(
    field,
    value,
    error,
):
    """
    check if valid duration
    """
    try:
        if pytimeparse_parse(value) is None:
            raise TypeError()

    except TypeError:
        error(field, f"'{value}' is not a valid duration.")


def is_date(
    field,
    value,
    error,
):
    """
    check if valid date
    """
    try:
        dateutil_parse(value)

    except Exception:
        error(field, f"'{value}' is not a valid date.")


# cerberus schema to validate project yaml file
proma_schema = {
    "name": {"type": "string", "required": True},
    "responsible": {"type": "string", "required": True},
    "start_date": {"type": "string", "required": True, "check_with": is_date},
    "end_date": {"type": "string", "required": True, "check_with": is_date},
    "events": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "name": {"type": "string", "required": True},
                "date": {
                    "type": "string",
                    "check_with": is_date,
                },
            },
        },
    },
    "workpackages": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "name": {"type": "string", "required": True},
                "responsible": {"type": "string", "required": True},
                "tasks": {
                    "type": "list",
                    "required": True,
                    "schema": {
                        "type": "dict",
                        "schema": {
                            "name": {"type": "string"},
                            "start_date": {
                                "type": "string",
                                "check_with": is_date,
                            },
                            "duration": {
                                "type": "string",
                                "check_with": is_duration,
                            },
                            "depends_on": {
                                "type": "string",
                            },
                            "milestones": {
                                "type": "list",
                                "schema": {
                                    "type": "dict",
                                    "schema": {
                                        "name": {"type": "string"},
                                        "responsible": {"type": "string"},
                                        "date": {
                                            "type": "string",
                                            "check_with": is_date,
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    },
}
