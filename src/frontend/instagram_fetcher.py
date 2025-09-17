import json
import httpx
import requests
from django.core.files.base import ContentFile
from .models import InstagramPost

client = httpx.Client(
    headers={
        "x-ig-app-id": "936619743392459",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "*/*",
    }
)

def scrape_user_posts(username: str, num_posts: int = 3):
    """Scrape Instagram user's recent posts and their details"""
    try:
        profile_result = client.get(
            f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}",
        )
        profile_result.raise_for_status()
        profile_data = json.loads(profile_result.content)
        posts = profile_data["data"]["user"]["edge_owner_to_timeline_media"]["edges"]
        formatted_posts = []
        for post in posts[:num_posts]:
            node = post["node"]
            if node["is_video"]:
                num_posts += 1
                continue
            import datetime
            from django.utils import timezone
            timestamp = node["taken_at_timestamp"]
            dt_taken = datetime.datetime.fromtimestamp(timestamp, tz=timezone.get_current_timezone())
            breakpoint()
            post_details = {
                "post_id": node["id"],
                "caption": node.get("edge_media_to_caption", {}).get("edges", [{}])[0].get("node", {}).get("text", ""),
                "short_code": node["shortcode"],
                "taken_date": dt_taken,
                "likes_count": node["edge_liked_by"]["count"],
                "comments_count": node["edge_media_to_comment"]["count"],
                "is_video": node["is_video"],
            }
            obj, created =InstagramPost.objects.update_or_create(
                post_id=post_details["post_id"],
                defaults=post_details
            )
            if not node["is_video"]:
                thumbnail_url = node.get("thumbnail_src", "")
                if thumbnail_url:
                    response = requests.get(thumbnail_url)
                    if response.status_code == 200:
                        # Save to ImageField
                        file_name = f"{node['id']}.jpg"
                        obj.thumbnail.save(file_name, ContentFile(response.content), save=True)
            formatted_posts.append(post_details)

        return formatted_posts

    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e}")
    except KeyError as e:
        print(f"Data parsing error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
