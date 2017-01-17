import base64

from tinydb import TinyDB

from Photo import Photo

db = TinyDB('db.json')


def create(photo):
    import base64
    str=''
    with open("test_folder/test_image1.png", "rb") as imageFile:
        str = base64.b64encode(imageFile.read())

    inserted = db.insert({'name': photo.name, 'photo': str})
    print ("Photo inserted: \n{0}\n".format(db.get(eid=inserted)))

    return inserted


def update(photoId, photo):
    db_photo = db.get(eid=photoId)
    print("Photo to update:\n{0}\n".format(db_photo))
    db.update({'name': photo.name, 'photo': photo.photo}, eids=[photoId])
    print("Updated photo: \n{}\n".format(db.get(eid=photoId)))


def read(photo_id):
    print("Search photo with id {}".format(photo_id))
    photo = db.get(eid=photo_id)
    print ("Photo found:\n{}\n".format(photo))
    return photo


def delete(photo_id):
    photo = db.remove(eids=[photo_id])
    print ("Photo removed:\n{}\n".format(photo))

#
# pid = create(Photo(0, 'name', 'photo'))
# update(pid, Photo(1, 'UpdatedName', "UpdatedPhoto"))
# print ("Read photo:\n{}\n".format(read(pid)))
# delete(pid)
# print ("Read photo:\n{}\n".format(read(pid)))
