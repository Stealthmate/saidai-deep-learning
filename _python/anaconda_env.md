---
layout: default
title: Anacondaで環境を作る
toc: true
last_edit: 2019-10-30
---

# 事前知識・準備

{% assign lnk = site.python | where: "url", "/python/anaconda.html" | first %}
- [{{ lnk.title }}]({{ lnk.url | relative_url }})
- Anacondaが既に使えるようになっている
- ユーザー名が`michael`だと仮定する

# Anacondaで環境を作る

Anacondaで環境を作る時、以下のコマンドを使います。

```bash
conda create --name <env_name>
```

ここで、`<env_name>`は環境を識別するための名前で、半角英数からなる文字列です。以下、環境名が`myenv`だと仮定して行きますが、どうぞ好きな名前にしてください。

ターミナルでは現在恐らく以下のようなprompt（コマンドの前にくる部分）が表示されています。

```bash
(base) michael@michael-pc:
```

ここにある`(base)`というのは、今使っている環境の名前を指しています。Anacondaがデフォルトで使う環境の名前が`base`なので、今`base`環境にいることがわかります。

では、`myenv`に切り替えるのにどうすればいいでしょう？答えは、以下のコマンドです：

```bash
conda activate myenv
```

これで、promptの頭が`(myenv)`に変わるはずです。また、もし`base`に戻りたかったら、以下のコマンドでできます。

```bash
conda deactivate
```

# Anacondaのパッケージについて

Anacondaからは、**パッケージ**という、ライブラリやプログラム等をインストールすることができます。Anacondaのサイトでは、パッケージは**channel**（チャンネル）という、供給源で分類されます。チャンネルを特に指定しない場合は、`anaconda`というチャンネルが使われますが、ライブラリやプログラムによっては、`anaconda`にはない物もあります。何がどこにあるかを知るためには、[Anacondaのrepository](https://anaconda.org/anaconda/repo){:target="_blank"}のサイトを検索すると良いでしょう。

# pythonパッケージをインストールする

Anacondaでパッケージをインストールしたい時は以下を使います:

```bash
conda install [ -c <channel> ] <package>
```

では、pythonをインストールしてみましょう。`python`は`anaconda`チャンネルにあるので、チャンネルを指定しなくても問題ありません。以下のいずれかのコマンドでインストールできます。

```bash
conda install python
conda install -c anaconda python
```

これを実行すると、Anacondaはいくつかのリストを表示してくれます。文字がいっぱいあって凄まじいと思うかもしれませんが、良くみてみると、以下の行があります：

- `The following packages will be DOWNLOADED` - これは、Anacondaがパッケージをインストールするためにダウンロードするもの
- `The following packages will be INSTALLED` - これは、Anacondaがパッケージをインストールするために、追加でインストールしなければいけないもの
- `The following packages will be DOWNGRADED` - これは、Anacondaがバッケージを古いバージョンに戻すもの
- `The following packages will be UPGRADED` - これは、Anacondaがパッケージを新しいバージョンに更新するもの

では、何故`python`だけをインストールしたいのに、こんなにも色々入れたり更新したりしなければいけないのでしょう？実は、ライブラリというのも、他のライブラリの力を借りています。なので、一つのパッケージをインストールしようとすると、ほとんどの場合は他にもインストールしなければいけないことが多いです。更には、パッケージAがパッケージBの力を借りているとき、パッケージBのバージョンを厳密に指定しなければいけないのです。場合によっては、バージョンを調整しなければいけないこともあるので、古いものに戻したり更新したりする必要も出てきます。

# 心想学習のためのパッケージをインストールする

心想学習などで良く使うパッケージをここで列挙しておきますので、各自でインストールしてみましょう。[Anacondaのrepository](https://anaconda.org/anaconda/repo){:target="_blank"}でチャンネルの確認を忘れないよに。

- `numpy` - ベクトルや行列計算用のライブラリ
- `pandas` - 表データを扱うためのライブラリ
- `scipy` - 数学や科学のためのライブラリ*
- `matplotlib` - 図を描くためのライブラリ
- `seaborn` - 図を綺麗に描くためのライブラリ
- `scikit-learn` - 機械学習やディープラーニングを行うためのライブラリ
- `keras` - （GPUで）ディープラーニングを行うためのライブラリ
