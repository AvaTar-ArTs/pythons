import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.http


def authenticate():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secrets.json"
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, ["https://www.googleapis.com/auth/youtube.upload"],
    )
    credentials = flow.run_local_server()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials,
    )
    return youtube


def upload_video(youtube, file_path, title, description):
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {"categoryId": "22", "description": description, "title": title},
            "status": {"privacyStatus": "public"},
        },
        media_body=googleapiclient.http.MediaFileUpload(file_path),
    )
    response = request.execute()
    print(f"Uploaded {file_path} with title '{title}'")


def generate_title_description(index, specific_fact):
    title = f"Spooky Fact #{index}: {specific_fact} #Shorts"
    description = f"Unveiling spooky fact #{index}: {specific_fact}. Stay tuned for more! #HalloweenHistory #Shorts"
    return title, description


def main():
    youtube = authenticate()
    directory_path = os.path.expanduser(
        "/Users/steven/Movies/Spooky Tales/short-spook2/vids2",
    )
    video_files = [f for f in os.listdir(directory_path) if f.endswith(".mp4")]

    specific_facts = [
        "The first Jack O'Lanterns were made from turnips",
        "Halloween was influenced by an ancient Roman festival",
        # ... [Add more facts as per your videos]
    ]

    for i, (filename, specific_fact) in enumerate(zip(video_files, specific_facts)):
        title, description = generate_title_description(i + 1, specific_fact)
        file_path = os.path.join(directory_path, filename)
        upload_video(youtube, file_path, title, description)


if __name__ == "__main__":
    main()
