from elasticsearch7 import Elasticsearch, helpers
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import re
import warnings

warnings.simplefilter("ignore") # 屏蔽 ES 的一些Warnings

nltk.download('punkt')  # 英文切词、词根、切句等方法
nltk.download('stopwords')  # 英文停用词库

def to_keywords(input_string):
    """
    将输入字符串转换为关键字列表
    """
    no_symbols = re.sub(r'[^a-zA-Z0-9\s]', '', input_string)
    word_tokens =word_tokenize(no_symbols)

    stop_words = set(stopwords.words('english'))

    ps = PorterStemmer()
    filter_sentence = [ps.stem(w) for w in word_tokens if not w in stop_words]
    return ''.join(filter_sentence)
