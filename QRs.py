import cypher
import segno
import os

path = ""
list_of_images = []


# Path and dir
def set_path(new_path: str) -> None:
    """Sets the working folder path and updates the list of images."""
    global path
    path = new_path
    global list_of_images
    list_of_images = get_list()


def get_list() -> list:
    """Returns a list of images located in the working folder."""
    global path
    list_of_files = []
    for file in os.listdir(path):
        if file[-4:] == ".png":
            list_of_files.append(file[:-4])
    return list_of_files


# Create and delete an image
def new_qr(name: str, visitor_id: str, visitor_number: int) -> None:
    """Creates a PNG image of a QR code from text (name - name of the file with the event)."""
    qrcode = segno.make_qr(cypher.encrypt_number(visitor_id + str(visitor_number), cypher.get_gamma_filename(name)))
    qrcode.save(f"{path}{visitor_id}{visitor_number}.png", dark=(0, 0, 0), light=(255, 255, 255))


def remove_qr(name: str) -> None:
    """Deletes an image with the selected name."""
    global path
    os.remove(f"{path}{name}.png")
