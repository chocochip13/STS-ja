#import pandas as pd
import numpy as np
import re
from tqdm._tqdm_notebook import tqdm_notebook as tqdm
tqdm.pandas()

puncts = [',', '.', '`','"', ':', ')', '。','(','ー','・', '-','／', '!', '?', '|', ';', "'", '$', '&', '/', '[', ']', '>', '%', '=', '#', '*', '+', '\\', '•',  '~', '@', '£',
 '·', '_', '{', '}', '©', '^', '®', '`',  '<', '→', '°', '€', '™', '›',  '♥', '←', '×', '§', '″', '′', 'Â', '█', '½', 'à', '…', '\n', '\xa0', '\t',
 '“', '★', '”', '–', '●', 'â', '►', '−', '¢', '²', '¬', '░', '¶', '↑', '±', '¿', '▾', '═', '¦', '║', '―', '¥', '▓', '—', '‹', '─', '\u3000', '\u202f',
 '▒', '：', '¼', '⊕', '▼', '▪', '†', '■', '’', '▀', '¨', '▄', '♫', '☆', 'é', '¯', '♦', '¤', '▲', 'è', '¸', '¾', 'Ã', '⋅', '‘', '∞', '«',
 '∙', '）', '↓', '、', '│', '（', '»', '，', '♪', '╩', '╚', '³', '・', '╦', '╣', '╔', '╗', '▬', '❤', 'ï', 'Ø', '¹', '≤', '‡', '√', ]


html_tags = ['<p>', '</p>', '<table>', '</table>', '<tr>', '</tr>', '<ul>', '<ol>', '<dl>', '</ul>', '</ol>',
             '</dl>', '<li>', '<dd>', '<dt>', '</li>', '</dd>', '</dt>', '<h1>', '</h1>',
             '<br>', '<br/>', '<strong>', '</strong>', '<span>', '</span>', '<blockquote>', '</blockquote>',
             '<pre>', '</pre>', '<div>', '</div>', '<h2>', '</h2>', '<h3>', '</h3>', '<h4>', '</h4>', '<h5>', '</h5>',
             '<h6>', '</h6>', '<blck>', '<pr>', '<code>', '<th>', '</th>', '<td>', '</td>', '<em>', '</em>']

empty_expressions = ['&lt;', '&gt;', '&amp;', '&nbsp;',
                     '&emsp;', '&ndash;', '&mdash;', '&ensp;'
                     '&quot;', '&#39;']

other = ['span', 'style', 'href', 'input']

dict = {
        '０' : '0', '１' : '1', '２' : '2', '３' : '3', '４' : '4',
        '５' : '5', '６' : '6', '７' : '7', '８' : '8', '９' : '9',
        'Ａ' : 'A', 'Ｂ' : 'B', 'Ｃ' : 'C', 'Ｄ' : 'D', 'Ｅ' : 'E',
        'Ｆ' : 'F', 'Ｇ' : 'G', 'Ｈ' : 'H', 'Ｉ' : 'I', 'Ｊ' : 'J',
        'Ｋ' : 'K', 'Ｌ' : 'L', 'Ｍ' : 'M', 'Ｎ' : 'N', 'Ｏ' : 'O',
        'Ｐ' : 'P', 'Ｑ' : 'Q', 'Ｒ' : 'R', 'Ｓ' : 'S', 'Ｔ' : 'T',
        'Ｕ' : 'U', 'Ｖ' : 'V', 'Ｗ' : 'W', 'Ｘ' : 'X', 'Ｙ' : 'Y',
        'Ｚ' : 'Z', 'ａ' : 'a', 'ｂ' : 'b', 'ｃ' : 'c', 'ｄ' : 'd',
        'ｅ' : 'e', 'ｆ' : 'f', 'ｇ' : 'g', 'ｈ' : 'h', 'ｉ' : 'i',
        'ｊ' : 'j', 'ｋ' : 'k', 'ｌ' : 'l', 'ｍ' : 'm', 'ｎ' : 'n',
        'ｏ' : 'o', 'ｐ' : 'p', 'ｑ' : 'q', 'ｒ' : 'r', 'ｓ' : 's',
        'ｔ' : 't', 'ｕ' : 'u', 'ｖ' : 'v', 'ｗ' : 'w', 'ｘ' : 'x',
        'ｙ' : 'y', 'ｚ' : 'z', '－' : '-', '、' : ', ', '　' : ' ',
         '／' : '/','？' : '?', '｀' : '`'}


def pre_preprocess(x):
    return str(x).lower()

def rm_spaces(text):
    spaces = ['\u200b', '\u200e', '\u202a', '\u2009', '\u2028', '\u202c', '\ufeff', '\uf0d8', '\u2061', '\u3000', '\x10', '\x7f', '\x9d', '\xad',
              '\x97', '\x9c', '\x8b', '\x81', '\x80', '\x8c', '\x85', '\x92', '\x88', '\x8d', '\x80', '\x8e', '\x9a', '\x94', '\xa0',
              '\x8f', '\x82', '\x8a', '\x93', '\x90', '\x83', '\x96', '\x9b', '\x9e', '\x99', '\x87', '\x84', '\x9f',
             ]
    for space in spaces:
            text = text.replace(space, ' ')
    return text

def remove_urls(x):
    x = re.sub(r'(https?://[a-zA-Z0-9.-]*)', r'', x)

    # original
    x = re.sub(r'(quote=\w+\s?\w+;?\w+)', r'', x)
    return x

def clean_html_tags(x, stop_words=[]):
    for r in html_tags:
        x = x.replace(r, '')
    for r in empty_expressions:
        x = x.replace(r, ' ')
    for r in stop_words:
        x = x.replace(r, '')
    return x

def replace_num(text):
    text = re.sub('[0-9]{5,}', '', text)
    text = re.sub('[0-9]{4}', '', text)
    text = re.sub('[0-9]{3}', '', text)
    text = re.sub('[0-9]{2}', '', text)
    return text

def get_url_num(x):
    pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    urls = re.findall(pattern, x)
    return len(urls)


def clean_puncts(x):
    for punct in puncts:
        x = x.replace(punct, f' {punct} ')
    return x

#zenkaku = '０,１,２,３,４,５,６,７,８,９,（,）,＊,「,」,［,］,【,】,＜,＞,？,・,＃,＠,＄,％,＝'.split(',')
#hankaku = '0,1,2,3,4,5,6,7,8,9,q,a,z,w,s,x,c,d,e,r,f,v,b,g,t,y,h,n,m,j,u,i,k,l,o,p'.split(',')

def clean_text_jp(dict, x):
    x = x.replace('。', '')
    x = x.replace('・', '')
    x = x.replace('ー', '')
    x = x.replace('／', '')
    x = x.replace('！', '')
    x = x.replace('、', '')
    x = x.replace('’','')
    x = x.replace('\n', '') # 改行削除
    x = x.replace('\t', '') # タブ削除
    x = x.replace('\r', '')
    m = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))
    x = m.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], x)
    x = re.sub(re.compile(r'[!-\/:-@[-`{-~]'), ' ', x)
    x = re.sub(r'\[math\]', ' LaTex math ', x) # LaTex削除
    x = re.sub(r'\[\/math\]', ' LaTex math ', x) # LaTex削除
    x = re.sub(r'\\', ' LaTex ', x) # LaTex削除
    #for r in zenkaku+hankaku:
     #   x = x.replace(str(r), '')
    x = re.sub(' +', ' ', x)
    return x

def clean_empty(x):
    x = x.replace(r'^\s*$', np.nan, regex=True)
    x = x.dropna()
    return x


def cleaning(data):
    data = data.progress_apply(lambda x: pre_preprocess(x))
    data = data.progress_apply(lambda x: rm_spaces(x))
    data = data.progress_apply(lambda x: remove_urls(x))
    data = data.progress_apply(lambda x: replace_num(x))
    data = data.progress_apply(lambda x: clean_html_tags(x, stop_words=other))
    data = data.progress_apply(lambda x: clean_text_jp(dict,x))
    data = data.progress_apply(lambda x: clean_puncts(x))
    data = clean_empty(data)
    return data