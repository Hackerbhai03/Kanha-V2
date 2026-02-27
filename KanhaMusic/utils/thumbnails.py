import random

# 🔥 Tumhare diye hue images
RANDOM_THUMBS = [
    
    "https://files.catbox.moe/vbdda6.jpg",
    "https://files.catbox.moe/3up9ky.jpg",
    "https://files.catbox.moe/jktiak.jpg",
    "https://files.catbox.moe/0n4439.jpg",
    "https://files.catbox.moe/l2id2z.jpg",
    "https://files.catbox.moe/l2id2z.jpg",
    "https://files.catbox.moe/8c6zfn.jpg",
    "https://files.catbox.moe/to3v10.jpg",
    "https://files.catbox.moe/mcqu0j.jpg",
    "https://files.catbox.moe/2803m5.jpg",
    "https://files.catbox.moe/gf3142.jpg",
    "https://files.catbox.moe/gcqh0j.jpg"
    
]

_last_thumb = None

async def get_thumb(videoid=None):  # videoid ignore
    global _last_thumb

    try:
        choice = random.choice(RANDOM_THUMBS)

        # ❌ same image repeat na ho
        while choice == _last_thumb and len(RANDOM_THUMBS) > 1:
            choice = random.choice(RANDOM_THUMBS)

        _last_thumb = choice
        return choice

    except Exception as e:
        print(e)
        return RANDOM_THUMBS[0]
