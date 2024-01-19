import cypher
import segno
import os

path = ""


# Path and dir
def set_path(new_path: str) -> None:
    """Sets the working folder path."""
    global path
    path = new_path


# Create and delete an image
def new_qr(name: str, visitor_id: str) -> None:
    """Creates a PNG image of a QR code from text (name - name of the file with the event)."""
    qrcode = segno.make_qr(cypher.encrypt_number(visitor_id, cypher.get_gamma_filename(name)))
    qrcode.save(f"{path}{visitor_id}.png", dark=(0, 0, 0), light=(255, 255, 255), scale=15)


def remove_qr(visitor_id: str) -> None:
    """Deletes an image with the selected name."""
    global path
    os.remove(f"{path}{visitor_id}.png")


# QR code reading
def decipher_qr(name: str, text: str) -> str:
    """Returns the encrypted visitor id (name - name of the file with the event)."""
    code = cypher.encrypt_number(text, cypher.get_gamma_filename(name))
    for i in code:
        if i not in "1234567890":
            return ""
    return code
