import os
from pyrogram import Client
from pyrogram.errors import RPCError

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")

app = Client("my_session", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)


def parse_link(link: str):
    """
    Parse Telegram message link into (chat_id, msg_id).
    Supports both public and private (t.me/c/...) links.
    """
    try:
        if "t.me/c/" in link:
            parts = link.split("/")
            chat_id = int("-100" + parts[-2])   # private/supergroup
            msg_id = int(parts[-1])
            return chat_id, msg_id
        elif "t.me/" in link:
            parts = link.split("/")
            username = parts[-2]               # public channel username
            msg_id = int(parts[-1])
            return username, msg_id
        else:
            raise ValueError("❌ Invalid link format")
    except Exception as e:
        print("❌ Link parsing failed:", e)
        return None, None


async def process_link(link: str):
    chat_id, msg_id = parse_link(link)
    if not chat_id:
        return False

    try:
        msg = await app.get_messages(chat_id, msg_id)
        print("✅ Message fetched:", msg)

        if msg.document:
            print("📄 File found:", msg.document.file_name, msg.document.mime_type)
            path = await msg.download("downloads/")
            print("💾 Saved at:", path)
            return True
        else:
            print("⚠️ No document in this message")
            return False

    except RPCError as e:
        print("❌ Telegram API error:", e)
        return False
    except Exception as e:
        print("❌ Unexpected error:", e)
        return False


async def main():
    links = [
        # yahan apne test links daalo
        "https://t.me/c/123456789/45",
        # "https://t.me/publicchannel/123"
    ]

    success = 0
    for link in links:
        ok = await process_link(link)
        if ok:
            success += 1

    print(f"🎯 Batch Completed ✅ Success: {success}/{len(links)}")


if __name__ == "__main__":
    app.run(main())
