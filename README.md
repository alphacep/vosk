# For Kaldi API for Android and Linux please see [Vosk API](https://github.com/alphacep/vosk-api). This is a server project.

This is Vosk, the lifelong speech recognition system.

## Concepts

As of 2019, the neural network based speech recognizers are pretty
limited in terms of amount of the speech data they can use in training
and require enormous computing power and time to train and optimize the
parameters. Neural networks have problems with human-like one shot
learning, their decisions are not very robust to unseen conditions and
hard to understand and correct.

That is why we decided to build a system based on large signal database
concept. We apply audio fingerprinting scheme. The audio is segmented on 
chunks, the chunks are stored in the database based on LSH hash value. 
During decoding we simply lookup the chunks in the database to get the
idea what are the possible phones. That helps us to make a proper decision
on decoding results.

The advantages of this approach are:

  - We can quickly train on 100000 hours of speech data on very simple hardware
  - We can easily correct recognizer behavior just by adding samples
  - We can make sure that recognition result is correct because it is sufficiently
    represented in the training dataset
  - We can parallelize training across thousands of nodes
  - We support lifelong learning paradigm
  - We can use this method together with more common neural network training to improve recognition accuracy
  - The system is robust against noise

The disandvantages are:

  - The index is really huge, it is not expected to fit a memory of single server
  - The generalization capabilities of the model are quite questionable, at the same time
    the generalization capabilities of the neural networks are also questionable.
  - For now the segmentation requires conventional ASR, but in the future we might segment ourselves.

The nice to have things in the future would be:

  - Multilingual training
  - Our own segmentation
  - The tool to reduce the model to fit the mobile
  - Specialized hardware to implement this AI paradigm

## Usage

To install the requirements run

```
pip3 install -r requirements.txt
```

To prepare the training/verification data create the following two files:

  - `wav.scp` list to map uterances to wav files in filesystem
  - `phones.txt` the CTM file with phonemes and timings. It could be CTM file from the alignment or
    it could be a CTM file from the decoding

You can create them with [Kaldi ASR toolkit](http://kaldi-asr.org)

### Indexing

To add the data to the database run

```
python3 index.py wavs-train.txt phones-train.txt data.idx
```

That will add the data to the database data.idx or create a new one

### Verification

To verify decoding results run

```
python3 verify.py wavs-test.txt phones-test.txt data.idx
```

The tool will search for segments in the index and report suspicious
segments which you can additionally check and later add to the database
to improve the accuracy of recognition.

### Related papers and links

 - [VOSK presentation at NSU (in Russian)](https://www.youtube.com/watch?v=gsOMU1UTF7s)
 - [Memory, Modularity, and the Theory of Deep Learnability. Google Tech Talk by Rina Panigrahy](https://www.youtube.com/watch?v=bP5oyH_5nMU) shows importance of memory for learning complex functions.
 - [Large Language Models in Machine Translation by Thorsten Brants at al.](https://aclweb.org/anthology/D07-1090.pdf) Google's paper on simple backoff terascale LM.
 - [Deep Learning of Binary Hash Codes for Fast Image Retrieval by Kevin Lin at al.](https://www.iis.sinica.edu.tw/~kevinlin311.tw/cvprw15.pdf) a nice deephash [implementation](https://github.com/flyingpot/pytorch_deephash)
 - [Episodic Memory in Lifelong Language Learning](https://arxiv.org/pdf/1906.01076.pdf)
 - [Extreme Classification in Log Memory using Count-Min Sketch: A Case Study of Amazon Search with 50M Products](https://arxiv.org/abs/1910.13830)
 - [On-device Supermarket Product Recognition](https://ai.googleblog.com/2020/07/on-device-supermarket-product.html) Google's good example of kNN for mobile search
 - [Hash-Routed Neural Networks](https://github.com/ma3oun/hrn) Great idea and solid math
 - [Towards Lifelong Learning of End-to-end ASR](https://arxiv.org/pdf/2104.01616.pdf) Methods get more publicity
