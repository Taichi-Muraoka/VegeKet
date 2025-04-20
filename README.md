# 環境構築

## git clone
任意のフォルダで  
```
git clone git@github.com:Taichi-Muraoka/VegeKet.git
```


## 仮想環境構築
クローン後のプロジェクトフォルダ内に移動  
フォルダ名変えてる場合は合わせてください。  
```
cd Vegeket
```

以下コマンド実行
```
python3 -m venv venv
```
後半の`venv`は任意でも可  
このドキュメント上は`venv`とした場合で説明していく  

仮想環境を有効化
```
source venv/bin/activate
```

※無効化する場合は
```
deactivate venv/bin/activate
```


## 必要なパッケージをインストール
```
pip install -r requirements.txt
```


## envファイルの設定
`secret`フォルダ直下に`.env.example.dev`をコピーした`.env.dev`を作成する  

<img width="193" alt="image" src="https://github.com/user-attachments/assets/ad30a44b-f2e5-40e0-818f-d802dcdb593b" />

#### `SECRET_KEYの設定`
`.env.dev`内の`SECRET_KEY`に任意の文字列を設定する（複雑な文字列推奨）  
```
SECRET_KEY="hogehogehogehoge&%hogehogehogehoge&%hogehogehogehoge"
```

#### `STRIPE_API_SECRET_KEY`の設定

stripeにログインして以下のようにシークレットキーをコピーして貼り付ける  
https://stripe.com/jp

<img width="1447" alt="image" src="https://github.com/user-attachments/assets/ad896518-8010-4960-a7e0-98176fe50c2c" />

<img width="1010" alt="image" src="https://github.com/user-attachments/assets/179fab52-31e0-4659-a01f-ef182fd9ba8d" />


## makemigration
以下コマンドでマイグレーションを実行する
```
python manage.py makemigrations
```
```
python manage.py migrate
```


## サーバーを立ち上げる
以下コマンドでサーバーを立ち上げる
```
python manage.py runserver
```

http://localhost:8000

<img width="1466" alt="image" src="https://github.com/user-attachments/assets/6ae7791f-bc56-436b-93a8-b78f09eb42d2" />

#### 管理画面
http://localhost:8000/admin

<img width="678" alt="image" src="https://github.com/user-attachments/assets/375ab4c1-dcfc-45a3-b2ae-026d364f018c" />
