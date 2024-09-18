def prepare(url):
    url = url.replace('/open?', '/uc?')  # google drive
    url = url.replace('dl=0', 'dl=1')  # dropbox
    return url
