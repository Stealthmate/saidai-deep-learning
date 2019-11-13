---
layout: default
title: "Emacsの設定を変えてみる"
series: Emacs on Steroids
series_part: 2
published: 2019-11-14
last_edit: 2019-11-14
toc: true
---

{% assign lnk = site.linux | where: "url", "/linux/emacs-on-steroids-01-basics.html" | first %}

[前回]({{ lnk.url | relative_url }})では、Emacsの中にElispのインタプリタがあり、ほとんどの動作はElispで書かれたスクリプトの実行結果だと述べました。また、ショートカットの書き方や特徴についても述べました。今回は実際にElispを書きながら、Emacsの動作を変えて、新しいショートカットを作ってみます。

# 事前知識・準備

- [{{ lnk.title }}]({{ lnk.url | relative_url }})
- ユーザー名が`michael`だと仮定する

# Emacsの設定ファイル

Emacsが起動するとき、`init.el`というファイルをまず最初にload（ロード・実行）します。`init.el`は普段、`~/.emacs.d/init.el`にあります。もし存在しなければ、作っておきましょう。

```bash
cd ~/.emacs.d/
touch init.el
```

`init.el`の拡張子に注目しましょう。`.el`というのは予想通りElispから来ています。つまり、`init.el`はElispで書かれたスクリプトです。

# `init.el`に書く内容

では、`init.el`に一体何を書けばいいでしょうか。簡単に言うと、命令を書きます。Pythonで`x = 3`と各のと同じように、Elispでも変数を定義したり、値を変更したり、処理を呼び出したりできます。少し抽象的に言うと、Emacsの**状態**を**変更**させます。例えば、文字の色が変数`char-color`に保存されているとしたら、その変数の値を`yellow`に変えることでEmacsの状態を変え、次に画面を描くときにEmacsがその新しい状態を使って、黄色い文字を描いてくれます。

## 行番号が常に表示されるように設定してみる

テキストエディターを使うとき、行番号が表示されると位置を把握しやすいですね。Emacsではデフォルトで行番号が表示されないので、表示されるようにしましょう。そのために、`init.el`で以下を書きます：

```elisp
(global-display-line-numbers-mode t)
```

`init.el`を保存して、Emacsを再起動してみてまた`init.el`を開いてみましょう。左側に行番号が表示されているはずです。

---

では、上記のコードについて少し解説をしておきましょう。

まず、Elispでは全ての命令がカッコで囲まれます。なぜかと言うと、Elispのコードは全てリストから成るからです（豆知識：Lispという名前は**Lis**t **P**rocessor（列処理機）が由来です）。Elispで各リストはカッコで囲まれ、それぞれの要素をスペース区切りで書きます。なので、上のコードは2つの要素からなるリストで、それぞれ`global-display-line-numbers-mode`と`t`です。

`global-display-line-numbers-mode`というのは、名前から分かると思いますが、`global`で（どこでも）`line numbers`（行番号）を`display`（表示）するモードです。一方`t`というのは`true`という値を表しています。つまり、`global-display-line-numbers-mode`を`true`にすることで、常に行番号が見えるようになります。

さてこれは変数の代入でしょうか。実は違います。変数の代入についてはまた次の節で解説しますが、上記の文は**関数の呼び出し**です。Elispでは、リストの頭に来る要素は常に関数の名前です。したがって、上記の文は、`global-display-line-numbers-mode`という関数を呼び出し、それに`t`という値を変数として渡しています。

では、`global-display-line-numbers-mode`はどのような関数でしょうか。[前回]({{ lnk.url | relative_url }})説明した通り、`describe-function`（あるいは`C-h f`）を使うと、説明が出てきます。

> Toggle Display-Line-Numbers mode in all buffers.
>
> With prefix *ARG*, enable Global Display-Line-Numbers mode if *ARG* is positive;
>
> otherwise, disable it. If called from Lisp, enable the mode if *ARG* is omitted or nil.

全てのバッファー（開いているファイル）で、`Display-Line-Numbers mode`を有功にしてくれるそうです。さらに、もし引数を渡したら、それが正であれば有功にし、それ以外の場合を無効にしてくれるそうですね。なお、もし引数を渡していなければ、デフォルトで有功にしてくれると書いてあります。

## Emacsの起動画面を無くしてみる

Emacsを起動するとき、このような画面が出てきますよね

{% capture emacs_startup_screen %}assets/images/{{ page.url | remove_first: ".html" }}/emacs-startup-screen.png
{% endcapture %}
![Emacs Startup Screen]({{ emacs_startup_screen | absolute_url }})

綺麗には見えますが、あまり使いみちがないですね。この画面を表示せずに、即タイピング可能な状態で起動するようにしてみましょう。`init.el`に以下を書いて、保存して、Emacsを再起動してみましょう：

```elisp
(setq inhibit-startup-message t)
```

画面が消えていますね！

---

では、先程と同様に上の文を分析しましょう。今までの知識を使うと以下のことがいえます：

* この文は`setq`関数を呼び出している
* `setq`関数に引数`inhibit-startup-message`と`t`という2つの引数を渡している。

では、`setq`関数について調べてみましょう。`C-h f setq RET`を打つと：

> (setq [*SYM* *VAL*]...)
>
>
> Set each *SYM* to the value of its *VAL*.
>
> The symbols *SYM* are variables; they are literal (not evaluated).
>
> The values **VAL** are expressions; they are evaluated.
>
> Thus, (setq x (1+ y)) sets ‘x’ to the value of ‘(1+ y)’.
>
> The second *VAL* is not computed until after the first *SYM* is set, and so on;
>
> each *VAL* can use the new value of variables set earlier in the ‘setq’.
>
> The return value of the ‘setq’ form is the value of the last *VAL*.

少し複雑ですが、要するに`SYM`の値を`VAL`に設定するということを言っています。真ん中らへんに書いてる例を見ると、`(setq x (1+ y))`は`x`に`(1+ y)`の値を代入すると書いてあります。

つまり、変数への代入も関数呼び出しで行っています。

---

変数に値を代入する方法はこれでわかったと思います。しかし、値を代入している変数がそもそもどのようなものか、どこで使われてどのような値を取らなければいけないかは分からないですよね。そういうときに、`describe-function`とほとんど同じ`describe-variable`関数が役に立ってくれます！文字通り、`describe-variable`はある変数について教えてくれます。そしてショートカットは`C-h v`です。

*Pro Tip: `C-h f`や`C-h k`と同様に、`C-h v`を**h**elp **v**ariableとして考えれば覚えやすいです！*

では、`inhibit-startup-message`について調べてみましょう。`C-h v inhibit-startup-message RET`を打つと：

> Documentation:
>
> Non-nil inhibits the startup screen.

簡単ですね。`nil`以外の値は起動画面を無効にするそうです。

# Emacsをスッキリさせるための簡単なカスタマイズ

Emacsを起動すると、上に他のソフトと同じメニュー（ファイル、編集、設定など）がありますね。更にその下に良く使う昨日のボタンがあり、画面の右側にスクロールバーもありますね。Emacsにある程度慣れれば、これらはむしろ邪魔だと思うようになります。なぜかと言うと、ショートカットを使いこなせていれば、わざわざマウスを動かしてボタンを押す動作をする必要がないからです。

皆さんに是非Emacsにそれぐらい慣れてほしいので、そのきっかけとして、上の3つのものを全部非表示にするためのカスタマイズ設定を載せておきます。それぞれ以下の通りです：

```elisp
(menu-bar-mode -1) ;; メニューを消す
(tool-bar-mode -1) ;; ボタンバーを消す
(scroll-bar-mode -1) ;; スクロールバーを消す
```

*Pro Tip: Elispでは`;;`で行コメントが書けます！*

上で説明した知識の範囲内なので、ぜひ各自でそれぞれの関数が何をしているか調べてみてください！

# まとめ

今回は`init.el`について説明し、簡単なElispの書き方を勉強しました。関数の呼び出しと変数の代入についてやり方を解説しまし、簡単なカスタマイズ設定をいくつか紹介しました。次回は、Emacsの様々な*mode*について解説したいと思います。
