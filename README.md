Originally from [clovaai](https://github.com/clovaai/deep-text-recognition-benchmark)
## Non-Latin language datasets.
1. Create your own lmdb dataset.
```
pip3 install fire
python3 create_lmdb_dataset.py --inputPath data/ --gtFile data/gt.txt --outputPath result/
```
The structure of data folder as below.
```
data
├── gt.txt
└── test
    ├── word_1.png
    ├── word_2.png
    ├── word_3.png
    └── ...
```
At this time, `gt.txt` should be `{imagepath}\t{label}\n` <br>
For example
```
test/word_1.png Tiredness
test/word_2.png kills
test/word_3.png A
...
```
2. Modify `--select_data`, `--batch_ratio`, and `opt.character`, see [this issue](https://github.com/clovaai/deep-text-recognition-benchmark/issues/85).

### Create lmdb
```
python3 create_lmdb_dataset.py --inputPath /home/jw/data/ocrdata/ko/ --gtFile /home/jw/data/ocrdata/ko/val.txt --outputPath /home/jw/data/ocrdata/ko/lmdb/val/
```

## Training 학습 
OCR 은 3 band 필요 없다. 1 band 만 해도 충분하다.
* `--rgb` default=False
* `--input_channel` default=1,
```
python3 train.py --exp_name 0530 --train_data /home/jw/data/ocrdata/ko/lmdb/train --valid_data /home/jw/data/ocrdata/ko/lmdb/val --select_data MJ-ST --batch_ratio 0.9-0.1 --Transformation TPS --FeatureExtraction ResNet --SequenceModeling BiLSTM --Prediction Attn --output_channel 512 --hidden_size 512 
```
### Fine Tune
```
python3 train.py --exp_name 0417 --train_data /home/jw/data/ocrdata/en/lmdb/ko/train --valid_data /home/jw/data/ocrdata/en/lmdb/ko/val --select_data MJ-ST --batch_ratio 0.9-0.1 --Transformation TPS --FeatureExtraction ResNet --SequenceModeling BiLSTM --Prediction Attn --saved_model "saved_models/0416/best_accuracy.pth" --FT 
```



## 모델 테스트
1. CRAFT 돌리기: 
python test.py --trained_model=./weights/craft_mlt_25k.pth --test_folder=/home/jw/data/test/
2. code/ocrdata/_util.py extract_bbox_folder() 이용해서 text를 crop 해줌
```
python3 demo.py --Transformation TPS --FeatureExtraction ResNet --SequenceModeling BiLSTM --Prediction Attn --output_channel 512 --hidden_size 512 --saved_model saved_models/0517/best_accuracy.pth --image_folder /home/jw/data/test/가격표/ 
```

## License
Copyright (c) 2019-present NAVER Corp.


