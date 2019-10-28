---
layout: default
title: 日本語入力の設定
---

## 必要なパッケージをインストールする

```bash
sudo apt install fcitx fcitx-mozc fcitx-tools
```

## 言語パッケージをインストールする

タスクバーのMenuから`Input Method -> Input Method -> Japanese -> Install`をクリックする。

## ログアウトし、再びログインする

## mozcを設定する

- タスクバーのMenuから`Fcitx Configuration -> Input Method -> +`をクリックする
- `Only Show Current Language`を外す
- `mozc`を探して、選択する

## 日本語入力の使い方

`CTRL-Space`で英語・日本語に切り替えができます。ひらがなで文字を打ち、スペースで変換できます。

## その他設定

### 全角半角キーで切り替える

タスクバーMenuから、`Fcitx Configuration -> Global Config`に行き、`Trigger Input Method`で`CTRL-Space`をクリックし、全角半角キーを押す。
