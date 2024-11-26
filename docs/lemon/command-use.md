# 各コマンド使用方法

以下は、LemonBotの各コマンドとその使用方法です。

## レモンコイン系コマンド

#### `/about-lemoncoin`
- **説明**: Lemoncoinについて見ます。
- **使用例**: `/about-lemoncoin`

---

#### `/login-bonus`
- **説明**: 2時間に1回、ログインボーナスとして500レモンコインを獲得できます。
- **使用例**: `/login-bonus`
- **制限**: 2時間に1回使用可能。

---

#### `/coin-balance`
- **説明**: 自分の現在のレモンコイン残高を確認します。
- **使用例**: `/coin-balance`

---

#### `/transfer-coin recipient:<ユーザー名> amount:<金額>`
- **説明**: 他のユーザーにレモンコインを譲渡します。
- **使用方法**:
  - `recipient:` には、譲渡先のユーザー名を入力します。
  - `amount:` には、譲渡するレモンコインの金額を入力します。
- **使用例**: `/transfer-coin recipient:john amount:100`

---

#### `/coin-ranking`
- **説明**: レモンコインを最も多く持っている上位5人のユーザーを表示します。
- **使用例**: `/coin-ranking`
- **返答例**:
  ```
    レモンコインランキング
    上位5人のレモンコイン所持者
    順位 1
    sample1: 9519 コイン
    順位 2
    sample2: 6921 コイン
    順位 3
    sample3: 5318 コイン
    順位 4
    sample4: 2835 コイン
    順位 5
    sample5: 1948 コイン

  ```

---
#### `/gacha`
- **説明**: 1000レモンコインでガチャを引きます。開発者もあまり理解していません。
---

## 便利系コマンド

#### `/help-command`
- **説明**: すべてのコマンド一覧を表示します。
- **使用例**: `/help-command`
---

#### `/base64 action:<encode/decode> content:<内容>`
- **説明**: 入力したコンテンツをBase64エンコードまたはデコードします。
- **使用方法**:
  - `action:` には、`encode` または `decode` を指定します。
  - `content:` には、エンコードまたはデコードしたい文字列を入力します。
- **使用例**:
  - エンコード: `/base64 action:encode content:HelloWorld`
  - デコード: `/base64 action:decode content:SGVsbG9Xb3JsZA==`

---

#### `/afk-start message:<メッセージ>`
- **説明**: AFK（離席）状態にして、他のユーザーに通知するメッセージを設定します。
- **使用方法**:
  - `message:` には、離席中に通知したいメッセージを入力します。
- **使用例**: `/afk-start message:今席を外しています。`

---

#### `/afk-end`
- **説明**: AFK（離席）状態を解除します。
- **使用例**: `/afk-start message:今席を外しています。`

---

#### `/ping`
- **説明**: pingします。botをメンションしても同じことができます。
- **使用例**: `/ping`

---

#### `/announce`
- **説明**: botのアナウンスを読みます。
- **使用例**: `/announce`

---

#### `/join-message action: message:`
- **説明**: 参加メッセージを表示します。メッセージ管理権限以上の人が実行できます。
- **プレースホルダ**: 以下のプレースホルダが使用できます。
  - {member.name}: 参加したメンバーの名前
  - {member.id}: 参加したメンバーのID
- **使用例**: `/announce`

---

## ネタ系コマンド

#### `/lemon`
- **説明**: ランダムに一つレモンの品種を出力します。
- **使用例**: `/lemon`

---

#### `/about-lemoncoin`
- **説明**: Lemoncoinについて見ます。
- **使用例**: `/about-lemoncoin`

---

#### `/5000 top: bottom:`
- **説明**: 5000兆円ほしいジェネレーターです。
- **使用例**: `/5000 top:5000兆円 bottom:ほしい！`
- **使用API**: https://github.com/CyberRex0/5000choyen-api

---

## Bot管理者専用

#### `/coin-admin action: target_user: amount:`
- **説明**: レモンコインの管理者コマンドです。
- **使用例**: `/coin-admin action:send target_user:@techfish_1 amount:1`

