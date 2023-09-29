import json
import pathlib

import requests
import requests.cookies

import colab_research_google_com_api as CRGCA


def main():
    # constants
    user_email, notebook_id, cookies = json.loads(pathlib.Path("config.json").read_text("utf-8")).values()
    session = requests.Session()
    session.cookies = requests.cookies.cookiejar_from_dict(CRGCA.cookies_to_dict(cookies))
    origin = "https://colab.research.google.com"
    notebook_url = origin + "/drive/" + notebook_id

    # identity crafting
    sapisidhash = CRGCA.craft_sapisidhash(session, origin)
    drive_api_key = CRGCA.extract_drive_api_key(session, notebook_url)
    notebook_name = CRGCA.get_notebook_revisions(session, drive_api_key, sapisidhash, notebook_id)["items"][-1]["originalFilename"]
    ccu_info = CRGCA.ccu_info(session)  # needed to get the tunnel
    tunnel = CRGCA.get_assign_tunnel(session, notebook_id)

    if "endpoint" not in tunnel.keys():
        raise Exception("Go to '" + notebook_url +
                        "' and complete the captcha before executing the script.")

    ws_session = CRGCA.get_notebook_ws_session(session, tunnel["endpoint"], notebook_name, notebook_id)

if __name__ == "__main__":
    main()
