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

