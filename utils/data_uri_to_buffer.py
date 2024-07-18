import base64

def data_uri_to_buffer(uri):
    if not uri.startswith('data:'):
        raise TypeError('`uri` does not appear to be a Data URI (must begin with "data:")')

    # Strip newlines
    uri = uri.replace('\r\n', '').replace('\n', '')

    # Split the URI up into the "metadata" and the "data" portions
    first_comma = uri.index(',')
    if first_comma == -1 or first_comma <= 4:
        raise TypeError('malformed data: URI')

    # Remove the "data:" scheme and parse the metadata
    meta = uri[5:first_comma].split(';')
    base64_encoded = 'base64' in meta
    data = uri[first_comma + 1:]

    if base64_encoded:
        buffer = base64.b64decode(data)
    else:
        buffer = data

    return buffer