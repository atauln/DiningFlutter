import requests
import json


def get_locations():
    try:
        response = requests.get("https://tigercenter.rit.edu/tigerCenterApp/tc/dining-all?date=2023-03-06")
    except ConnectionError:
        print("didn't work, L")

    locations = json.loads(response.content).get("locations")
    


if __name__ == "__main__":
    main()
