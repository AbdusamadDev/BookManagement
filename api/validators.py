def validate_fields(*columns, **request_data):
    # mustnt be null or blank
    # must include all fields
    for key, value in request_data.items():
        