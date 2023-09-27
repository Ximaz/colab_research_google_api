import requests
import requests.cookies

import colab_research_google_com_api

def main():
    session = requests.Session()
    cookies = colab_research_google_com_api.cookies_to_dict(colab_research_google_com_api.get_cookies("cookies.txt"))
    session.cookies = requests.cookies.cookiejar_from_dict(cookies)
    origin = "https://colab.research.google.com"
    sapisidhash = colab_research_google_com_api.craft_sapisidhash(session, origin)
    notebook_id = "<NOTEBOOK_ID>"
    user_email = "<GMAIL_EMAIL_ADDRESS>"
    notebook_url = origin + "/drive/" + notebook_id
    drive_api_key = colab_research_google_com_api.extract_drive_api_key(session, notebook_url)
    ccu_info = colab_research_google_com_api.ccu_info(session) # needed to get the tunnel
    tunnel = colab_research_google_com_api.get_assign_tunnel(session, user_email, notebook_id)

    # Discontinued from now on because recaptache and botguard protects Colab from bot trying to open
    # websockets for code execution.

if __name__ == "__main__":
    main()
