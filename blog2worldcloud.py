import os
import matplotlib.pyplot as plt
import os
import argparse
import jieba
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
from argparse import ArgumentParser
from imageio import imread
jieba.enable_parallel(4)

parser = argparse.ArgumentParser(description="make world cloud with blog summary")
parser.add_argument("-t", "--text", help="blog summary text", default="blog.txt", type=str)
parser.add_argument("-f", "--font_path", help="the path of font", default="SourceHanSerifK-Light.otf", type=str)
parser.add_argument("-sw", "--stop_words", help="the stop words file path", default="stop_words.txt", type=str)
parser.add_argument("-o", "--output_image", help="the output path", default="world_cloud.png", type=str)
args = parser.parse_args()

def jieba_processing_txt(text):
    mywordlist = []
    seg_list = jieba.cut(text, cut_all=False)
    liststr = "/ ".join(seg_list)

    with open(args.text, encoding='utf-8') as f_stop:
        f_stop_text = f_stop.read()
        f_stop_seg_list = f_stop_text.splitlines()

    for myword in liststr.split('/'):
        if not (myword.strip() in f_stop_seg_list) and len(myword.strip()) > 1:
            mywordlist.append(myword)
    return ' '.join(mywordlist)


def load_file2list(filename):
    with open(filename, 'r') as fn:
        flines = fn.readlines()
        datam = []
        for line in flines:
            
            temp = line.strip('\n').split(' ')[0]
            datam.append(temp)
    return datam

if __name__ == '__main__':
    
    text = open(args.text).read()
    font_path = args.font_path
    
    jieba_result = jieba_processing_txt(text)
    mask_list = load_file2list(args.stop_words)

    mask_word = STOPWORDS.union(mask_list)

    wc = WordCloud(font_path=font_path, background_color="white", max_words=400,
                   max_font_size=400, width=2000, height=1000, stopwords=mask_word)
    wc.generate(jieba_result)
    wc.to_file(args.output_image)