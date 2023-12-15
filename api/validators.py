def validate_fields(*columns, **request_data):
    # mustnt be null or blank
    # must include all fields
    for field in columns:
        