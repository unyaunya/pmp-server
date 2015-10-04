# PMP-Server

すぐ忘れるのでメモ


## 動作環境
   Python3.3+Flask(いろいろ)+SQLAlchemy

## 動かし方

起動：

    > run.py

　　デフォルトはhttp://localhost:5000で動く(Flaskのデフォルト)


DB作成：

    > db_create.py

　　これでスキーマ作成

    > db_firstuser.py

　　これでデフォルトユーザ(admin/admin)を作成。こいつやんないとログインできない

スキーマ管理：

    > db_migrate.py

    > db_downgrade.py

    > db_upgrade.py

　　(すでに忘れてる)

## フォルダ構成

 - config.py
 - db_create.py
 - db_downgrade.py
 - db_firstuser.py
 - db_migrate.py
 - db_upgrade.py
 - manage.py
 - requirements.txt
 - run.py
 - instance/
 - migrations
 - pmpserver/
  -  __init__.py
  -  forms.py
  -  models.py
  - views.py
  - admin/
  - datadictionary/
  - login/
  - userprofile/
  - util/
  - static/
  - templates/
