# HYPERDEEP
Hyperdeep is a proof of concept of the deconvolution algorithm applied on text.
It use a standard CNN for text classification, and include one layer of deconvolution for the automatic detection of linguistic marks. This software is integrated on the Hyperbase web platform (http://hyperbase.unice.fr) - a web toolbox for textual data analysis.

# requirements:
- python3
- keras + tensorflow

# HOW TO USE IT
# data
Datas are stored in the data/ folder. The training set should be splited into phrases of fixed length (50 words by default). And each phrase should have a label name at the begining of the line. A label is written : __LABELNAME__
Hyperdeep is distributed with an example of corpus named Campagne2017 (in data/Campagne2017). This is a french corpus of the 2017 presidential election in france. There are 5 main candidates encoded with the labels (Melenchon, Hamon, Macron, Fillon, LePen).

# train skipgram
You can train a skipgram model (word2vec) by using the command :
	$ python hyperdeep.py skipgram -input data/Campagne2017 -output bin/Campagne2017.vec
This command will create a file named Campagne2017.vec in the folder bin (create the folder if needed). This txt is the vectors file of the training data.

# test skipgram
the skipgram model can be tested by using the command (example with the word France) :
	$ python hyperdeep.py nn bin/Campagne2017.vec France

# train classifier
To train the classifier:
	$ python3 hyperdeep.py train -input data/Campagne2017 -output bin/Campagne2017
The command will create bin/Campagne2017.index for the vocabulary and bin/Campagne2017 for the model

# test the classifier
Then you can make predictions on new text. There is an example in bin/Campagne2017.test. It's a discourse of E. Macron as french president on 31th december 2017. Hyperdeep will split the discourse in fixed length phrases and should predict most of the phrase a E. Macron
	$ python hyperdeep.py predict bin/Campagne2017 bin/Campagne2017.vec data/Campagne2017.test

# Observe the deconvolution
The predict command line will create a result file in the folder result/ (create the folder if needed). This file is a json format file where you can find the activation score given by the deconvolution for each word. An example of results is given in result/Campagne2017.test.res

# Experiments

```
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -U --force-reinstall keras==1.1.4
python3 -m pip install -U --force-reinstall keras==2.0.0
python3 -c "import keras; print(keras.__version__);"
mkdir bin/
```

## TRAIN SKIPGRAM
```
python hyperdeep.py skipgram -input data/Campagne2017 -output bin/Campagne2017.vec
```

## TESTING
```
python hyperdeep.py nn bin/Campagne2017.vec France

[('rayonne', 0.625952959060669), ('fière', 0.6240432262420654), ('puissante', 0.6158779263496399), ('coexistence', 0.615835428237915), ('gagnante', 0.6157932281494141), ('fraternelle', 0.6106721758842468), ('façonné', 0.6029340028762817), ('traversé', 0.6028076410293579), ('forte', 0.6014634370803833), ('mosaïque', 0.5977412462234497)]


TRAINING CLASSIFIER
python3 hyperdeep.py train -input data/Campagne2017 -output bin/Campagne2017

TEST CLASSIFIER
python hyperdeep.py predict bin/Campagne2017 bin/Campagne2017.vec data/Campagne2017.test

----------------------------
DECONVOLUTION
----------------------------
(3, 128, 1, 512)
(3, 128, 1, 512)
DECONVOLUTION SHAPE :  (101, 50, 128, 1)
101
```

```
cat results/Campagne2017.test.res | json_pp

[
   {
      "sentence" : "::11.593507766723633 le:16.891237258911133 choix:47.93613815307617 du:35.58413314819336 peuple:65.93293762207031 français:64.55390930175781 ,:55.15997314453125 votre:42.49549865722656 choix:56.94794845581055 par:34.339454650878906 lequel:29.816349029541016 vous:30.37843132019043 m':26.36418914794922 avez:34.59223175048828 <PAD>:69.55484008789062 votre:45.25927734375 confiance:60.548038482666016 et:36.16371154785156 avec:28.190982818603516 elle:36.694664001464844 votre:40.45203399658203 impatience:94.9781723022461 ,:56.47802734375 vos:33.44449234008789 exigences:32.770057678222656 ,:31.24873924255371 vos:32.61974334716797 attentes:28.31665802001953 ;:101.72959899902344 j':23.938312530517578 en:21.642822265625 suis:23.090648651123047 pleinement:25.462093353271484 conscient:31.470001220703125 .:29.107559204101562 Aussi:54.604217529296875 ,:56.7678337097168 depuis:38.937042236328125 mon:22.68429946899414 élection:45.78916549682617 en:22.658348083496094 mai:34.11579513549805 dernier:46.26791000366211 ,:46.37293243408203 je:28.92486572265625 me:28.759069442749023 suis:36.3964729309082 attaché:44.55897903442383 à:19.251060485839844 simplement:12.999951362609863 ",
      "prediction" : [
         5.47782474313863e-05,
         0.00010245582961943,
         0.997055888175964,
         0.00185899913776666,
         0.000927872606553137
      ]
   },
…
]
```