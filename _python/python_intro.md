---
layout: default
title: Python即入門
toc: true
---

# 事前知識・準備

{% assign lnk = site.python | where: "url", "/python/anaconda_env.html" | first %}
- [{{ lnk.title }}]({{ lnk.url | relative_url }})
- Anacondaが既に使えるようになっている
- ユーザー名が`michael`だと仮定する

# CとPythonの違い

CとPythonは基本的に全く違うものです。その違いについて、以下2つの観点から説明します。

## コンパイラvsインタープリタ

C言語は`gcc`でコンパイルしますよね。具体的に言うと、`.c`フィアルから`gcc`を使って実行ファイルを作ります。この動作が何故必要なのかというと、実行ファイルに書いてある内容はCPUが直接解釈・実行する命令なので、C言語からその命令を生成するのにコンパイラが必要です。

一方、pythonはコンパイルする必要がありません。しかし、pythonコードを実行する時、`python foo.py`というように実行することに注目してください。この時、「実行」されているのはファイルではなく、`python`プログラムです。そして`python`プログラムに`foo.py`という引数が渡されています。ここで何が起こっているのかというと、`python`プログラムが`foo.py`に書いている内容を臨時的にその場で命令を解釈して、それに対応した動作を行います。

他の言い方をすると、`python`プログラムはコンパイルされた実行ファイルであり、その入力として`foo.py`に書いてある内容が渡され、入力に対して`python`プログラムが何かをして、結果を出力します。このような挙動で動くものを**interpreter** (和：通訳者）と言い、インタープリタが命令を**evaluate （評価）**すると言います。

## 低級言語vs高級言語

次の問題を考えます。

> あるアルファベットの文字列が与えられた時、その中にある全ての`a`文字を`bc`で置き換えたい。つまり`abc`という入力に対して`bcbc`を出力したい。

さて、これをC言語で実装するとどうなるでしょうか。ここでぜひ各自で答えを見る前に自分で考えてみてください。

---

大まかな流れを書くと、恐らく以下のような手順になります。

1. メモリを確保し、配列を作っておく。
2. 配列に入力された文字列を格納する。
3. `a`文字が出てくるインデックスを格納するためのメモリを確保し、配列を作っておく。
4. 入力文字列を辿り、`a`文字が出てくる所インデックスをインデックス配列に保存する。
5. 出力が保存される配列の必要メモリを計算し（文字が増える為）、確保し、配列を作っておく。
6. 入力文字列を辿り、`a`以外の文字を出力配列に保存し、`a`の代わりに`bc`文字列を保存する。
7. 出力文字列を出力する。

かなりめんどくさい手順になっています。メモリの確保や配列の管理等が特にめんどくさいですね。

では、`python`で書くとどうなるでしょうか。答えは：

```python
print( input().replace("a", "bc") )
```

以上です。簡単といえば簡単ですね。

---

上の問題で見たように、C言語とPython言語は**抽象度**、簡単に言えば**コードの細かさ**が違います。C言語だと一々細かく動作を書かなければいけないのに対し、Pythonでは色々な作業が予め用意されているし、メモリ管理などはしなくていいです。Pythonのように、**抽象度の高い**言語のことを**High-level language （高級言語）**と呼び、Cのように**抽象度の低い**（細かい）言語のことを**Low-level language（低級言語）**と呼びます。この高級とか低級というのは、決まった基準は特に無く、スペクトルみたいなものだと思ってください。Cが1だとして、Pythonが9ぐらいで、Javaは4、という風に捉えると良いででしょう。

## 静的型と動的型

C言語では変数や関数を定義するときに、その型を必ず定義しますよね。整数であれば`int`、実数であれば`double`等、型を定義して、違う型同士を足したり引いたりしようとすると、コンパイラが文句を言います。このような言語のことを**statically-typed language（静的型付け言語）**と言います。

一方、Pythonでは型を定義しません\*。というのは、変数をそのまま`x = 3`とだけ書いて、関数も`def f(x, y)`とだけ書きます。しかし、例えば文字列と文字列を割り算しようとすると、エラーが出ます。このような言語のことを**dynamically-typed language（動的型付け言語）**と言います。

では、PythonもCも型のミスでエラーが出るなら、何が違うの？と聞きたくなるでしょう。答えは、静的型付け言語は、プログラムを作る（コードをCPUへの命令に直す）時点で型をチェックし、文句を言います。一方Pythonのような動的型付け言語は、コードを実行する時点で文句を言います。一般的に静的型の方が安全でバグが少なくなるのですが、動的型の方が（インタプリタやコンパイラを作る人から見て）実装しやすくてシンプルです。


<div class="footnote">* 最近（[Python 3.8](https://docs.python.org/3/library/typing.html)）では定義できるようになってはいますが、あくまでも可読性を上げるためのものだけであり、守らないと文句を言われるようなものではありません。</div>

# Pythonを動かしてみる

Pythonはインタープリタ型言語（interpreted language）なので、先程言ったように、`python`プログラムが命令を解釈し実行します。インタープリタ型言語は多くの場合、わざわざプログラムをファイルに書き込んで、ファイルごと実行するという手順を追わなくても、1命令ずつ実行することができます。Pythonの場合、ターミナルで`python`とだけ打つと、インタープリタが起動します。インタープリタを起動してみて、以下の文を入力して、ENTERキーで実行してみましょう。

```python
1 + 3
```

結果は4になるはずです。C言語と同じように`+`, `-`, `*`, `/`, `%`演算が使えます。そして、Cとは違って、文字列に対してもいくつかの演算子が定義されています。以下のコマンドを打って、結果を確認しましょう。

```python
>>> "Saitama" + "-ken"
```

```python
>>> "bun" * 10
```

また、変数を定義して、変数で演算やその他の処理等もできます。

```
>>> x = 3
>>> x * 20
```

では、次の処理を行って見ましょう。ユーザー（入力）から名前（文字列）を受け取って、それに`-san`を付けたものを出力しましょう。Pythonでの入力は、`input()`関数で一行を読み取るようにできます。これを使うと：

```python
>>> name = input()
Valeri
>>> name + '-san'
```

## ファイル実行

これで基礎的な動作はひとまず以上ですが、インタプリタで一々命令をその場で書くだけでは、話になりませんね。では、ファイルを作成して実行してみましょう。Pythonで実行するファイルは、`.py`拡張子で保存します。

では、上で書いた手順をファイルに保存してみましょう（ここでは`program.py`だと仮定します）。

```python
name = input()
name + '-san'
```

では、実行して、入力してみましょう。

```
python program.py
Valeri
```

結果は出ましたか？恐らく出ていませんよね。上のように、インタプリタで直接命令を実行すると、その結果が自動的に表示されるようになっています。しかし、ファイルでは、自分から出力をしないと何も表示されません。つまり、所謂`printf`らしきものを使わないと、出力が出ません。Pythonでは、`print`関数で出力をします。では、上のプログラムを書き直すと：

```python
name = input()
print(name + '-san')
```
こう書くと結果が出るでしょう。


# リファレンスのためのサンプルコード

C言語と同様に、Pythonにもif文やfor文がありますが、書き方が少し違います。とはいえ、大して変わることはないので、以下のサンプルコードを読んで、使い方を覚えてください。

以下のプログラムは、Nまでの素数を順番にもとめて行くためのプログラムです。入力から整数Nを受け取って、素数を出力していきます。

```python
{% include_relative sample.py %}
```

[pyファイル]({{ "python/sample.py" | relative_url }})

# Python Documentation

Pythonは優れた[ドキュメンテーション](https://docs.python.org/3.7/)（マニュアルみたいなもの）がネットに上がっています。全て読むのは無理なので、必要に応じて参考していきましょう。ただし、自分のPythonと同じバージョンを見るようにしましょう。このリンクはバージョン3.7のものです。

全てを読むのは無理ですが、一旦[文字列](https://docs.python.org/3.7/library/stdtypes.html#text-sequence-type-str)に関するところをサラッと目を通しましょう。特に、`str.join()`や`str.find()`等、`str.<function>()`のような関数を軽く見てみてください（全部理解しなくてもいいです）。