import requests

def legal_entity_identiy_request(lei):
    if not lei:
        return None, 'No LEI Provided'

    params = {'lei': lei}
    r = requests.get('https://leilookup.gleif.org/api/v2/leirecords', params=params)

    if r.status_code == 400:
        return None, r.json().get('message')
    elif r.status_code != 200:
        return None, 'Invalid response from LEI API'

    if not r.json():
        return None, 'Invalid LEI'

    legal_name = r.json()[0].get("Entity").get("LegalName").get('$')
    return legal_name, None
