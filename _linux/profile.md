---
title: .profileと.bashrcの初期設定
layout: default
toc: true
last_edit: 2019-10-29
---

## 必要な知識

{% assign lnk = site.linux | where: "url", "/linux/environment_vars.html" | first %}
- [{{ lnk.title }}]({{ lnk.url | absolute_url }})

## 初期設定の意義

以下は、一般的に良く使われるプロフィール設定で、このブログではほぼ前提として扱うので、入れてしておきましょう。なお、随時更新していく予定なので、定期的に確認してください。

## .profileの設定

```bash
export PATH=$PATH:$HOME/bin:$HOME/.local/bin
eval `ssh-agent -s`
```

## .bashrcの設定
