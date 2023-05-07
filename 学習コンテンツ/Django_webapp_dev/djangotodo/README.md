process to build Django environment on Docker.

		Check the URL link below
		https://engineer-ninaritai.com/docker-django/

		Command I typed for it.
		~/docker/djangotodo ❯ subl Dockerfile
					FROM python:3
					RUN mkdir /code
					WORKDIR /code
					COPY requirements.txt /code
					RUN pip install -r requirements.txt
					COPY . /code/

		~/docker/djangotodo ❯ subl requirements.txt
					Django==3.0.7

		~/docker/djangotodo ❯ docker build -t djangotodo . --platform linux/x86_64

		~/docker/djangotodo ❯ docker run -v ~/docker/djangotodo:/code djangotodo django-admin startproject todoapp . --platform linux/x86_64

					~~ memo ~~
					-v　→ローカルPCのディレクトリとDockerコンテナのディレクトリを紐づけ
					~/docker/djangotodoのフォルダ（Djangoでtodoリストを作成するためのフォルダ）を、/codeのフォルダ（コンテナ内で開発する為のフォルダ）にマウントしている。
					どうやら、ファイルシステムのマウントの際はDockerImageの記述は不要?
					かめさんのDocker講座9-61ではImageも記述していた。
					実行してみたところ、自動的に作成した複数のDockerImageにファイルシステムがマウントされた。

					djangotodo　→先ほど作成したDockerイメージの指定
					django-admin admin startproject mysite .→Djangoで最初に入力するコマンド 　Dockerイメージの後にイメージで実行するコマンドを指定する
					~~ memo ~~


		~/docker/djangotodo ❯ docker run -v ~/docker/djangotodo:/code -d -p 8000:8000 djangotodo python manage.py runserver 0.0.0.0:8000

					~~ memo ~~
					最後に、もう一度”docker run”コマンドを入力して、Djangoを起動させます。
					Webブラウザで、
					http://127.0.0.1:8000
					とアクセスしてみましょう。djangoのページが表示されました！


					20230328
					このとき、もう８０００のポートが使われているというエラーが出たら、下のコマンドでDjandgoのrunserverを立ち上げられた。

					docker run --platform linux/x86_64 -v ~/docker/djangotodo:/code -d djangotodo python manage.py runserver 0.0.0.0:8000
					~~ memo ~~



ーーーーーーーーーーーーーーーーーーーーーーーーーー


Dockerコンテナへの入り方(標準的なアプローチ)
		~/docker/djangotodo ❯ docker run -it (イメージ名) bash

Dockerコンテナへの入り方（M1 Macで）
		~/docker/djangotodo ❯ docker run --platform linux/x86_64 -it (イメージ名) bash

	また、JupyterLabを起動時にスタートさせるDockerImage（8a31743d6dca）は、以下で実行すること。
		~/docker/djangotodo ❯
		docker run -v ~/docker/djangotodo:/code --platform linux/x86_64 -p 8888:8888 8a31743d6dca

	↑を実行したあとは、ウェブブラウザで以下を実行して、Jupyter Notebookを起動すること。
		localhost:8888
	↑ちゃんとファイルシステムをマウントしてあるので、
	~/docker/djangotodoの中身が更新されたら、コンテナ内のcode内も更新される。



Dockerコンテナからの抜け方
		# exit
			dockerのコンテナから抜けたいときexitを使うと基本的にはコンテナが終了してしまうので注意！
		# Ctrl+p Ctrl+q
			Dockerを起動させたままで抜ける


Docker build. のやり方(M1 Macで)
		~/docker/djangotodo ❯docker build --platform linux/amd64 .

					~~ memo ~~
					この「--platform linux/amd64」を書かないと、
					[exited code:1]としてエラーになり、Anacondaのインストールが途中で止まりエラーになる。
					参考URL：
					https://www.cloudnotes.tech/entry/m1mac-docker
					~~ memo ~~




ーーーーーーーーーーーーーーーーーーーーーーーーーー
django開発の始め方

1. プロジェクトを作成する。
	以下を実行することで、ディレクトリ直下にmanage.py等が生成され、サービス開発の基礎が構築される。
	# django-admin startproject todoapp .

2. アプリを１つ作成する。（Webサービスの中にある１つの機能）
	以下を実行することで、ディレクトリ直下にtodoappというディレクトリが生成され、ToDoアプリを作成する為の雛形が構築される。
	# python manage.py startapp todo

3. 初期設定を行う。（Udemyの動画内容の確認を推奨）
	1. 今後作成するHTMLファイルなどの保存場所を指定する。
		todoapp直下のsettings.pyの中身を変更する。
		TEMPLATESの中身の　dir型'DIRS':[]　に加筆する。

		BASE_DIRディレクトリの中に後で'templates'というディレクトリを作り、その中にHTMLファイルなどを保管する予定なので、以下のように変更する。

		'DIRS':[BASE_DIR / 'templates']

		その後、実際にBASE_DIRディレクトリ（ローカルホストで言うところのdjangotodoで、Dockerコンテナで言うところのcodeディレクトリのこと。）の中に'templates'というディレクトリを作る。

	2. 新たに作成したtodoというアプリを、アプリ一覧に追加する。
		todoapp直下のsettings.pyの中身を変更する。
		djangoのプロジェクトに対して、新しくアプリを作った際は、そのアプリを使うことを宣言するという目的で、以下を行う。
		list型のINSTALLED_APPSの中身のに、todoアプリを追加する。

		'todo.apps.TodoConfig'

	3. URLの繋ぎ込みを行う。
		todoapp直下のurls.pyの中身を変更する。
		WebアプリのURLに、ある特定の文字列が入ってきたとき、
		（例えばログインページなら、https://www.XXX.com/login みたいな文字列）
		どのアプリを参照するかを示す処理を、urls.pyの中に書く。（この例においてはログインページのアプリを参照することになるだろう。）

		list型のurlpatternsの中に、以下の追加する。
		今回は、既存の入力内容（adminという文字列が入っている時の処理）以外の文字列が入力された場合に参照する先を書く。（例外処理的な位置づけ）

		path('', include('todo.urls')),

		またこれに際して、includeというライブラリをインストールするコードも追加する。

		from django.urls import path, include

	4. todoアプリのディレクトリ内に、urls.py（アプリ）を作成する。
		3. で指定したアプリを実際に作成する必要がある。
		今回の位置づけ的には、このアプリは例外処理的なアプリであるはずなので、まぁ「このリンクは不正です」的なメッセージを表示するアプリになれば良さそう。

		作成したurls.pyの中に、以下を記述する。(超適当。どうあってもadminアプリが参照されるようになる。）

		from django.contrib import admin
		from django.urls import path, include

		urlpatterns = [
		    path('admin/', admin.site.urls),
		　]

	5.　models.pyを編集する。
		TodoModelのクラスを定義する。Todoアプリを作る際、どんな機能を実装するかをここに記述する。
		todoディレクトリの中のmodels.pyを、以下のコードを追加すると良い。

		class TodoModel(models.Model):
			title = models.CharField(max_length=100)
			memo = models.TextField()

	6. makemigrationsとmigrateをコマンド実行する。
		これはdjangoの機能の一つで、作成したアプリのバージョン管理をデータベースを使って行っているようなものだと思えば良い。（厳密には違うかも。）
		makemigrationsで、作成したアプリのデータベースを作成し、migrateでデータベースの中身を更新する。
		ちなみに自分で作成していないアプリ（プロジェクト構築時に自動生成されたadminやauth等）もこれで管理される。
		以下のコマンドを実行する。

		# python manage.py makemigrations
		# python manage.py migrate

	7. 管理画面（admin）を使ってみる。
		以下のコマンドを実行したあとに、adminアプリを参照して開いてみる。

		# python manage.py runserver

		ブラウザで以下のURLにアクセスする。

		http://127.0.0.1:8000/admin/login/?next=/admin/

		これでdjangoに標準で搭載されているadminアプリを実行できるはず。

		以下のコマンドを実行して、管理者権限を持つユーザー登録をしてみる。

		# python manage.py createsuperuser

		任意のユーザー名、PWを設定する。
		私は以下のように設定した。

		# Username (leave blank to use 'root'): gota
		# Email address: gotainu@gmail.com
		# Password: Nakazawa5

		これを使ってadminアプリのログインが行える。

	8. 管理画面（admin）に表示する情報を設定する。
		todoディレクトリのadmin.pyを参照して、以下を追加する。
		するとmodel.pyで構築したTodoモデルについての情報が、adminアプリ上で確認できるようになる。

		from .models import TodoModel
		admin.site.register(TodoModel)


	9. 管理画面（admin）でTodoモデルにダミーデータを追加してみる。
		ブラウザ上でadminアプリを開き（http://127.0.0.1:8000/admin/　）、Todo modelsにアクセスし（http://127.0.0.1:8000/admin/todo/todomodel/　）、タブの「Todo models」の右隣りにあり「＋add」を押下して、
		TitleとMemoに適当な情報を入力し、「SAVE」を押下する。
		するとタブの「Todo models」の中には、「Todo model onject(1)」が生成される。これがダミーデータである。

10. 管理画面（admin）で生成したダミーデータ名リストで確認する際、わかりやすい名前になるように設定してみる。
		現状だとダミーデータは、タブの「Todo models」の中に「Todo model onject(1)」と表示されているが、これだとわかりにくすぎる為、変更する。

		todoディレクトリ内のmodels.pyの中にある、class TodoModelの中身に以下の関数を追加する。

		def __str__(self):
        	return self.title

        すると、「Todo model onject(1)」という表示は「買い物」に書き換わっている。
        つまりtitleが表示される様になる。

 以上でかんたんな初期設定はおしまい。
 此処から先は、自分の作りたい物に沿って作っていこう。


ーーーーーーーーーーーーーーーーーーーーーーーーーー


自分で作ったDockerFile [image:8a31743d6dca]（20230212）

		FROM python:3
		RUN mkdir /code
		WORKDIR /code
		COPY requirements.txt /code
		RUN pip install -r requirements.txt
		RUN pip install --upgrade setuptools
		COPY . /code/

		WORKDIR /opt

		RUN apt-get update && apt-get install -y \
				wget \
				vim	

		RUN wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh && \
				sh Anaconda3-2022.10-Linux-x86_64.sh -b -p /opt/anaconda3 && \
				rm -f Anaconda3-2022.10-Linux-x86_64.sh

		ENV PATH /opt/anaconda3/bin:$PATH

		RUN pip install --upgrade pip
		WORKDIR /
		CMD ["jupyter","lab","--ip=0,0,0,0","--allow-root","--LabApp.token="]













