from base64 import b64encode


def get_auth_headers(username, password):
    return {
        'Authorization': 'Basic ' + b64encode(
            "{0}:{1}".format(username, password))
    }

# for testing
if __name__ == "__main__":
    print get_auth_headers("admin", "admin")
    print get_auth_headers("shashwat", "shashwat")