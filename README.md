# ydapi

Youdao Fanyi Command-Line Interface Using Youdao Api.

# Usage

1. `git clone https://github.com/O1sInfo/ydapi.git` or Download as zip.
2. (Optional) Put **yd.bat** in your envoiroment path.
3. Set some private value in **yd.py** such as `appKey`, `secretKey`. May you need a account. -> [有道API](http://ai.youdao.com/)
3. `yd -h` for HELP. 

# Example

* `yd -w word`
```
n        [语] 单词；话语；消息；诺言；命令,  (Word)人名；(英)沃德
vt       用言辞表达
```
* `yd -t 这是一段很长的文本，但不要超过5000字。 `
```
这是一段很长的文本但不要超过5000字。
--------------------------------------------------------------------------------
This is a long piece of text but not more than 5,000 words.
```
* `yd -f \file\path\to\translate -o \file\path\to\save`

