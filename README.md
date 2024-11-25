# LemonBot

新国産多機能BotのLemonBotです。  
開発主は時間がないのでChatGPTに頼っています。(ごめん)

---

## できること

- `/login-bonus`  
  ログインボーナスを受け取ります。
  
- `/coin-balance`  
  自分のレモンコイン残高を確認します。
  
- `/transfer-coin`  
  他のユーザーにレモンコインを譲渡します。
  
- `/coin-ranking`  
  レモンコインランキングを表示します。
  
- `/base64`  
  Base64エンコードまたはデコードします。
  
- `/afk-start`  
  AFK状態にする。通知したいことを設定できます。
  
- `/afk-end`  
  AFK状態を解除します。
  
- `/ping`  
  ボットのレスポンスを確認します。
  
- `/gacha`  
  レモンコイン1000でガチャを引きます。
  
- `/lemon`  
  ランダムにレモンの品種を表示します。
  
- `/announce`  
  現在のアナウンスを表示します。
  
- `/about-lemoncoin`  
  レモンコインについて説明します。
  
- `/5000`  
  5000兆円ほしいジェネレータです。
  
- `/coin-admin`  
  レモンコイン管理用コマンドです（管理者専用）。
  
- `/help-command`  
  LemonBotが提供するすべてのコマンドを表示します。

---

## 各cogsの内容

- **5000.py**  
  5000兆円ほしいジェネレーター  
  API powered by [5000choyen-api](https://github.com/CyberRex0/5000choyen-api)
  
- **AboutLemonCoin.py**  
  LemonCoin使用方法説明コマンドを実装
  
- **afk.py**  
  AFK通知を実装
  
- **base64.py**  
  Base64エンコード/デコードコマンドを実装
  
- **coin-Adjustment.py**  
  コインの小数を切り捨てるための実装
  
- **coin.py**  
  基本的なレモンコインの実装
  
- **gacha.py**  
  レモンコインを使ったガチャの実装
  
- **lemon.py**  
  ランダムなレモンの品種を出力するコマンドを実装
  
- **list.py**  
  コマンド一覧を出力するコマンドを実装
  
- **ping.py**  
  pingコマンドを実装
  
- **announce.py**  
  アナウンスコマンドを実装

---

## その他

LemonBotはユーザーの快適な体験を提供するために、さまざまな機能を組み合わせています。コマンドを使って、レモンコインの管理や、楽しいガチャ、AFK通知などを簡単に操作できます。

もし、使い方が分からなくなった場合は、`/help-command`を使ってください！

# 貢献してくれる皆さまへ

cogs/coin-admin.pyの中に、ユーザーIDがあります。
そこは、自分のIDに置き換えないと、/coin-adminが使えません。