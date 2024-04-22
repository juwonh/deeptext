import lmdb
from PIL import Image
import io
import string

def showimg():
    img_path = './data_lmdb_release/training/ST/img/'

    for index in range(403300,403400, 5):
        file_key = "image-%09d.jpg".encode() % index
        file_name = file_key.decode('utf-8')
        imfile= img_path + file_name

        im = Image.open(imfile)
        width, height = im.size
        print(str(width) + "x" + str(height))
        im.show()

# showimg()
        
print(len(string.printable[:-6]))