import lmdb
from tqdm import tqdm
import six
from PIL import Image
import os
from glob import glob

def read_lmdb(lmdb_file, img_save_dir, txtfile, rgb = True):
    lmdb_env = lmdb.open(
                lmdb_file,
                max_readers=32,
                readonly=True,
                lock=False,
                readahead=False,
                meminit=False,
            )
    txn = lmdb_env.begin(write=False)
    lmdb_cursor = txn.cursor()
    
    txt_file = open(txtfile,'w')
    
    nSamples = int(txn.get(b"num-samples"))
    print('Total Samples:%d'%nSamples)
    
    for index in tqdm(range(nSamples)):
        index += 1  # lmdb starts with 1
        label_key = "label-%09d".encode() % index
        label = txn.get(label_key).decode("utf-8")
        img_key = "image-%09d".encode() % index
        img_name = img_key.decode('utf-8')
        imgbuf = txn.get(img_key)
        
        buf = six.BytesIO()
        buf.write(imgbuf)
        buf.seek(0)
        
        if rgb:
            img = Image.open(buf).convert("RGB")  # for color image
        else:
            img = Image.open(buf).convert("L")
            
        img_file = img_save_dir + img_name+'.jpg'
        img.save(img_file)
        
        img_path_lst = img_file.split('/')[-2:]
        img_path_forward = '/'.join(img_path_lst)
        
        line = img_path_forward+' '+label+'\n'
        txt_file.write(line)
    txt_file.close()

def get_dir(path):
    dir_names = os.listdir(path)
    
    return dir_names

if __name__ == '__main__':
    
    lmdb_folder = './data_lmdb_release/training/MJ/MJ_train/'
    txtfile = lmdb_folder + '/txt.txt'
    img_save_dir = lmdb_folder + 'img/'
    
    if not os.path.exists(img_save_dir):
        print('Make Directory : %s'%img_save_dir)
        os.makedirs(img_save_dir)

    read_lmdb(lmdb_folder, img_save_dir, txtfile, rgb = True)