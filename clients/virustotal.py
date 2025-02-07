import vt, json

resource = open("./HiddenBot-py/resources.json")
data = json.load(resource)
key = data["VIRUSTOTAL_KEY"]

def getClient() -> None:
    vt_client = None
    try:
        vt_client = vt.Client(key, timeout = 30)
        print("Virustotal connection established")
    except Exception as e:
        print(e)
    return vt_client
