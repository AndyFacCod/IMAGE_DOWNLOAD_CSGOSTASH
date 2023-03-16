import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PIL import Image, ImageDraw

# Cuvantul cautat
special_word = "AK-47"

# Pagina web de la care dorim sa descarcam imaginile
url = "https://csgostash.com/weapon/" + special_word

# Directorul în care vor fi salvate imaginile
directory = "imagini-" + special_word

# Dimensiunea dorita pentru imaginea finala
final_size = (800, 800)

# Verificam daca directorul exista; daca nu, il cream
if not os.path.exists(directory):
    os.makedirs(directory)

# Descarcam pagina web folosind requests
response = requests.get(url)

# Verificam daca pagina a fost descarcata cu succes
if response.status_code == 200:

    # Parcurgem continutul paginii web folosind BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Identificam toate imaginile care contin special_word
    images = soup.find_all('img', alt=lambda x: x and special_word in x)

    # Descarcam fiecare imagine
    for image in images:

        # Construim URL-ul imaginii folosind functia urljoin
        image_url = urljoin(url, image["src"])

        # Descarcam imaginea folosind requests
        response = requests.get(image_url)
        image_url = f"{image_url}".split("_light_large")[0]
        image_url = image_url+ ".png"

        # Verificam daca imaginea a fost descarcata cu succes
        if response.status_code == 200:

            # Salvam imaginea in directorul dorit
            with open(os.path.join(directory, os.path.basename(image_url.split("?")[0])), "wb") as f:
                f.write(response.content)

            # Deschidem imaginea folosind biblioteca Pillow
            with Image.open(os.path.join(directory, os.path.basename(image_url.split("?")[0]))) as img:
                # Redimensionam imaginea la dimensiunea dorita
                img.thumbnail(final_size)

                # Cream un canvas de aceeasi dimensiune cu imaginea, si o facem transparenta
                canvas = Image.new("RGBA", final_size, (0, 0, 0, 0))

                # Plasam imaginea descarcata pe canvas
                canvas.paste(img, ((final_size[0] - img.size[0]) // 2, (final_size[1] - img.size[1]) // 2))

                # Salvam imaginea cu acelasi nume, dar cu extensia ".png" pentru a ne asigura ca este in formatul dorit
                canvas.save(os.path.join(directory, os.path.basename(image_url.split("?")[0])).split(".")[0] + ".png")

            print(f"Imaginea {image_url} a fost descarcata si modificata cu succes.")

        else:
            print(f"Imaginea {image_url} nu a putut fi descarcata.")
else:
    print("Pagina nu a putut fi descarcata.")
