

import requests
from io import BytesIO
from PIL import Image, ImageTk
import random
import tkinter as tk

def fetch_met_image():
    object_id = random.randint(100, 500000)
    url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"
    response = requests.get(url)
    data = response.json()

    if data.get("primaryImage"):
        return {
            "title": data["title"],
            "artist": data["artistDisplayName"],
            "image": data["primaryImage"]
        }
    else:
        return fetch_met_image()

def fetch_zen_quote():
    url = "https://zenquotes.io/api/random"
    response = requests.get(url)
    data = response.json()

    return {
        "quote": data[0]["q"],
        "author": data[0]["a"]
    }


def update_inspiration():
    image = fetch_met_image()
    quote = fetch_zen_quote()

    if "error" not in image: # I'm not sure how this error loop works
        response = requests.get(image["image"])
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        img = img.resize((200, 200))
        img = ImageTk.PhotoImage(img)

        label_image.config(image=img)
        label_image.image = img
    else:
        label_image.config(text="No image available")

    label_quote.config(text=f"\"{quote['quote']}\"\n- {quote['author']}")
    label_title.config(text=f"{image['title']} {image['artist']}")


window = tk.Tk()
window.title("Curating Inspiration")
window.geometry("600x600")
window.config(bg="#ffffff")

label_title = tk.Label(window, text="Inspiration Title", font=("Helvetica", 14, "bold"), bg="#ffffff", wraplength=380)
label_title.pack(pady=10)

label_image = tk.Label(window, bg="#f4f4f4")
label_image.pack(pady=20)

label_quote = tk.Label(window, text="Quote will be here", font=("Helvetica", 12), bg="#ffffff", wraplength=380, justify="center")
label_quote.pack(pady=10)

button_next = tk.Button(window, text="next", font=("Helvetica", 12), command=update_inspiration, bg="#000000", fg="white", relief="raised")
button_next.pack(pady=20)

update_inspiration()

window.mainloop()
