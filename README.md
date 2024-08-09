Originally from [clovaai](https://github.com/clovaai/deep-text-recognition-benchmark)

입력 이미지: 문자영역만 추출해서 crop한 이미지를 lmdb dataset으로 변환한 .mdb 파일을 사용.   
문자영역 crop 은 [CRAFT-pytorch](https://github.com/clovaai/CRAFT-pytorch)로 함

## 1 설치
```
git clone https://github.com/juwonh/ocr
cd ocr
python3 -m venv venv
pip install torch==2.0.1 torchvision==0.15.2 
pip install lmdb pillow nltk natsort
pip install fire
pip install opencv-python
```
## 2 데이터셋 준비 (optional)
### lmdb dataset 직접 만들기 : create_lmdb_dataset.py

데이터 폴더의 구조는 다음과 같다.
```
/home/jw/data/ocrdata/ko/
├── val.txt
└── val1
    ├── 0
        ├── 000002.jpg
        ├── 000004.png
        └── ...
└── val2
```
`gt.txt`의 컨텐츠는 다음과 같다: `{imagepath}\t{label}\n` <br>
예를 들어,
```
val1/0/000002.jpg   12
val1/11/110009.jpg  (Remaining>
val2/2/020011.jpg   춤닫업멸빙콥빙
...
```
```
python3 create_lmdb_dataset.py --inputPath /home/jw/data/ocrdata/ko/ --gtFile /home/jw/data/ocrdata/ko/val.txt --outputPath /home/jw/data/ocrdata/ko/lmdb/val/
```
## 3 학습 : train.py  

```
python3 train.py --exp_name 0809 --train_data /home/jw/data/ocrdata/ko/lmdb/train --valid_data /home/jw/data/ocrdata/ko/lmdb/val --imgH 96 --imgW 300 --select_data MJ-ST --batch_ratio 0.9-0.1 --Transformation TPS --FeatureExtraction ResNet --SequenceModeling BiLSTM --Prediction Attn --output_channel 512 --hidden_size 512 
```
* `--exp_name` saved_models 폴더 안에 exp_name 폴더가 생성되어 모델이 저장됨
* `--imgH` 학습할 이미지 높이 최대치 96 pixels (메모리 부족으로 32 pixels)
* `--imgW` 학습할 이미지 너비 최대치 300 pixels (메모리 부족으로 100 pixels)

### Fine Tune: (optional) 기존 모델에 이어 학습할 경우
```
python3 train.py --exp_name 0810 --train_data /home/jw/data/ocrdata/en/lmdb/ko/train --valid_data /home/jw/data/ocrdata/en/lmdb/ko/val --select_data MJ-ST --batch_ratio 0.9-0.1 --Transformation TPS --FeatureExtraction ResNet --SequenceModeling BiLSTM --Prediction Attn --output_channel 512 --hidden_size 512 --saved_model "saved_models/0809/best_accuracy.pth" --FT 
```

## 4 모델 QA
1. CRAFT-pytorch/test.py 돌리기: 
글자 bbox => 파일이름.txt 생성 
2. ocrdata/_util.py extract_bbox_folder() 이용해서 text를 crop 해줌

```
python3 demo.py --Transformation TPS --FeatureExtraction ResNet --SequenceModeling BiLSTM --Prediction Attn --output_channel 512 --hidden_size 512 --saved_model models/ko_0601.pth --image_folder /home/jw/data/ocrdata/test/가격표/ 
```
