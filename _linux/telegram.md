---
layout: default
title: Telegramの入れ方
---

## 事前準備

- 以下の手順で、ユーザーが`michael`だと仮定し、ホームディレクトリを`/home/michael`とします。各自自分のユーザーネームに合わせてください。

## Telegramをダウンロード

[ここ](https://desktop.telegram.org/)からTelegramをダウンロード（Linux 64-bit版）。以下の手順は`/home/michael/Downloads/tsetup.1.8.15.tar.xz`にダウンロードしたと仮定しますが、ファイル名が異なる場合は変えて適宜変更してください。

## Telegramのファイルを決まった場所に置く

Linuxでは、パッケージマネージャー（Mintは`apt`）以外の方法で取得したソフトは`/opt`に置くことが習慣です\*。なので、Telegramもそこに置きましょう。
ただし、`/opt`はHOMEディレクトリの外にあるので、特別な権限が必要です。そのために`sudo`を使います。以下はダウンロードしてからの手順です。なお、\#はコメントで、コマンドの動作には関係ありません。

```bash
sudo mkdir /opt/Telegram                                                                          # ディレクトリを作る
sudo tar -xvf /home/michael/Downloads/tsetup.1.8.15.tar.xz -C /opt/Telegram --strip-components=1  # .tar.xzというのは圧縮ファイルなので、/opt/Telegramで解凍します
sudo ln -s /opt/Telegram/Telegram /usr/bin/Telegram                                               # /usr/binはPATHに入っているので、/opt/Telegram/Telegramを指すリンクを/usr/binに置きます
```

最後の1行に注目してください。`ln`というプログラムはリンクを作るためのものです。リンクというのは、プログラムのように見せかけたものですが、実際はプログラムの場所を指しているだけです。大事なのは、`/usr/bin/Telegram`というリンクを実行すると、結果は`/opt/Telegram/Telegram`を実行したのと同じです。

<div class="footnote">
* ソースコードからビルドした物はまた別のところに置きます。
</div>

## TelegramをMenuで表示できるようにする

このままでもTerminalでTelegramを打てば使えますが、タスクバーのMenuに入れると起動しやすいですよね。

そのために、まずアイコンが必要ですね。Telegramから落としたものに残念ながらアイコンが入っていなかったので、自分達で落とす必要があります。幸い、ネットにはアイコンがあったので、

![telegram image](https://i.stack.imgur.com/OO565.png)

以下のコマンドでネットから画像を落とすことができます。

```bash
sudo curl https://i.stack.imgur.com/OO565.png -o /opt/Telegram/telegram128.png
```

`curl`というプログラムは、あるインターネットへのリンクから内容を落とします。

---


TelegramをMenuで表示するためには、`/usr/share/applications/`で新しいファイルを作らなければなりません。書式の説明は省略しますが、以下の内容のファイルを`/home/michael/telegram.desktop`という場所と名前で作りましょう。

```
[Desktop Entry]
Name=Telegram
Exec=/usr/bin/Telegram -- %u
GenericName=Messenger
Comment=Message your friends
Type=Application
Terminal=false
StartupNotify=false
Icon=/opt/Telegram/telegram128.png
```

これでほぼ完成です。後はファイルを指定した場所に移動するだけなので、以下のコマンドで終わらせましょう。

```
sudo mv /home/michael/telegram.desktop /usr/share/applications/
```

MenuでTelegramを打って見ましょう！
