---
title: Mirakurun + EPGStation on Debian 10 (Buster)
date: 2020-06-18 16:11
modified: 2020-09-17 17:22
author: Koichiro Yamada
category: development
tags: debian
slug: debian_mirakurun_epgstation
related_posts: 
cover: images/temp-cover.jpg
thumbnail: images/temp-thumbnail.jpg
summary: Debian GNU/Linux 10 Buster上でアースソフトのPT2を利用してテレビ番組録画環境を構築しました。MirakurunとEPGStationを使いこなせているかまでは不明です。
---

[link-debian-amd64-netinst]: https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/
[link-Mirakurun]: https://github.com/Chinachu/Mirakurun
[link-EPGStation]: https://github.com/l3tnun/EPGStation

[TOC]

# PCを使った録画環境

PCでテレビ番組を録画する際に必要なものはチューナーです。

私はずっとアースソフトのPT2を使っています。PC自体はNECのサーバであるExpress5800/S70タイプRB。いわゆる鼻毛鯖を2010年から使っていました。組み立ててしばらくしたら東日本大震災が発生してましたね。かれこれ10年経過していますがあっという間です。そしてPT2はまだまだ現役です。

2020年を前に、経年劣化しつつある各種部品の更新をかねて録画サーバーを更新しました。

当初はPCIスロットを装備したマザーボードで組んでみましたが、先を見越してPCI-ExpressスロットにPCI拡張カードを変換して利用することにしました。

|パーツ|製品|
|:---|:---|
|マザーボード|ASUS アスース H310M-E R2.0|
|CPU|Intel インテル BX80684G4920 [CPU Celeron G4920]|
|CPUクーラー|リテール品|
|メモリ|ADATA エーデータ DDR4-2666MHz CL19 288Pin DIMM デスクトップPC用メモリ 8GB×1枚|
|電源|ANTEC アンテック NE550 GOLD|
|SSD|A-DATA エーデータ ASU650SS-120GT-R [SSD 120GB]|
|HDD|手持ちの2TB|
|拡張ボード|AREA エアリア SD-PECPCiRi2 [拡張ボードの旧世主 第二章]|
|拡張ボード|アースソフト PT2|
|ケース|Thermaltake サーマルテイク Versa H18 |

上記構成で相性問題などはまった発生しませんでした。

エアリアの「拡張ボードの旧世主第二章」はPCIボードへの電源供給や固定するブラケットなどよく考えられた仕様だったので購入。もちろんPT2も動作確認できました。もう少しシンプルなものならAliExpressで2000円付近で入手可能なのでそちらでも良いと思います。ひと月も待てば届くはず。

問題が発生したのは当初用意したAntecの電源。NeoEcoシリーズの電源はSeasonic（シーソニック）のOEM品だから非常に高品質である！……なんてネットのレビューがありますが不具合続出でした。購入してファンを下向きにしケースに設置するとファンとファンガードが干渉してカラカラと音がなりました。工作精度がどうもよくない模様です。初期不良交換。

交換後の製品は異音の発生はないので運用開始。しかし、半年も経過すると原因不明な電源断が発生するようになりました。どうも内臓ハードディスクへのアクセスなどで負荷がかかるとストンと電源が落ちてしまうようです。状況を切り分けるのに数ヶ月かかりました……。日に日に動作状況が悪くなり、最後はSSDから煙。どうもSATAの電力供給に異常があるようでした。

こりゃダメだということで7年保証をいかそうと販売元に連絡するも新型コロナウイルスによる感染症のため営業時間が不安定になり修理依頼後ひと月を経過しても進捗がなし。（二ヶ月後に新品を手配いただきました……。）市場に新品在庫もないのがわかっているので、保証があてにならないと判断。別の電源を手配することにします。

Antecの電源は評判ほどよくはない。似たような不具合がぼちぼち見つかる。感染症のおかげで国内代理店のリンクスインターナショナルの対応も期待できずでした。残念無念です。

# debian Buster インストール

ずっと使っているDebian GNU/Linuxのインストールです。boとかpotatoなんかを使っていた頃から比べたら何も考えることはありませんね。非常に簡単になりました。

まず、Buster（Debian 10）のnetinstイメージを入手して、インストールUSBディスクを作成します。

macOS環境で作業する手順は次のとおり。

[Debian GNU/LinuxのカレントCDイメージ][link-debian-amd64-netinst]をダウンロードします。現行バージョンは10.4のようなので適宜実施。ブラウザが一番簡単じゃないだろうか。

```
$ cd ~/Downloads
$ curl -C - -L -O https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-10.4.0-amd64-netinst.iso
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   359  100   359    0     0    230      0  0:00:01  0:00:01 --:--:--   230
100  336M  100  336M    0     0  3064k      0  0:01:52  0:01:52 --:--:-- 3080k
```

isoファイルをimgファイルに変換します。

```
$ hdiutil convert -format UDRW -o ~/Downloads/debian-10.4.0-amd64-netinst.img ~/Downloads/debian-10.4.0-amd64-netinst.iso
Driver Descriptor Map（DDM：0） を読み込み中...
Debian 10.4.0 amd64 n           （Apple_ISO：1） を読み込み中...
Apple（Apple_partition_map：2） を読み込み中...
Debian 10.4.0 amd64 n           （Apple_ISO：3） を読み込み中...
EFI（Apple_HFS：4） を読み込み中...
.
Debian 10.4.0 amd64 n           （Apple_ISO：5） を読み込み中...
..............................................................................
経過時間： 3.992s
速度：84.1M バイト／秒
節約率：0.0%
created: /Users/YOUR_USER_NAME/Downloads/debian-10.4.0-amd64-netinst.img.dmg
```

差し込んでいるUSBメモリのデバイスを確認。（例は/dev/disk2の場合）

```
$ diskutil list
/dev/disk0 (internal, physical):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:      GUID_partition_scheme                        *128.0 GB   disk0
   1:                        EFI EFI                     209.7 MB   disk0s1
   2:                  Apple_HFS macOS                   127.2 GB   disk0s2
   3:                 Apple_Boot Recovery HD             650.0 MB   disk0s3
(略)
/dev/disk2 (external, physical):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:     FDisk_partition_scheme                        *4.0 GB     disk2
   1:             Windows_FAT_32 ESD-USB                 4.0 GB     disk2s1
```

USBメモリをアンマウント。（例は/dev/disk2の場合）

```
$ diskutil unMountDisk /dev/disk2
Unmount of all volumes on disk2 was successful
```

ddコマンドでimgファイルをUSBメモリに書き込み。（例は/dev/disk2の場合）

```
$ sudo dd if=~/Downloads/debian-10.4.0-amd64-netinst.img of=/dev/rdisk2 bs=1m
Password:
290+0 records in
290+0 records out
304087040 bytes transferred in 2.365862 secs (128531188 bytes/sec)
```

このとき、「/dev/disk2」ではなくて「/dev/rdisk2」の方が手早くコピーが終わる。シーケンシャルアクセスとランダムアクセスの関係ってやつと理解しています。

インストールUSBディスクが作成できたらLinuxマシンにUSBメモリを差し込んで起動する。お約束だけど内蔵しているSSDやHDDからブートしないためにも、BIOSの画面もたまには拝んで確認しておくのも良いことだと思います。

Debianインストーラーの操作については割愛します。

基本システムのみインストールすればいいので、デスクトップ環境やプリントサーバーなどのチェックを外してしまいます。スッキリ構成ならば5分くらいでインストールできてしまうことでしょう。やり直しだって気楽にできます。

# Debianインストール後

インストールできたらsudoとsshが利用できるようにします。

```
$ su -
# apt-get update
# apt-get install sudo openssh-server
# gpasswd -a YOUR_USER_NAME sudo
```

YOUR_USER_NAMEは適宜環境に応じて置換します。

sudoとsshさえ導入してしまえば、他の端末から操作できます。メモを見ながら作業なんてのはsshで端末に入った方が楽チンですからね。

LOCALEは日本語にしないのが自身の慣例なので、追加の設定。

```
$ sudo vi /etc/environment
```

```
LANG=en_US.utf-8
LC_ALL=en_US.utf-8
```

sshは公開鍵でのログインにします。作成した公開鍵をもとにauthorized_keysを適宜編集します。

```
$ ssh-keygen -t rsa
```

sshサーバーの設定は好みだと思いますが必要最低限からはじめます。

```
$ sudo vi /etc/ssh/sshd_config
```

```
PermitEmptyPasswords no
```

続いて、ソースリストの編集。これも好みです。国内の特定のミラーサーバを指定するよりは公式からのリダイレクト任せでもいいかなと思います。

```
$ sudo vi /etc/apt/sources.list
```

```
deb http://ftp.jp.debian.org/debian/ buster main contrib non-free
deb http://ftp.jp.debian.org/debian/ buster-updates main contrib
deb http://ftp.jp.debian.org/debian/ buster-backports main contrib non-free
deb http://security.debian.org/debian-security buster/updates main
deb-src http://ftp.jp.debian.org/debian/ buster main contrib non-free
deb-src http://ftp.jp.debian.org/debian/ buster-updates main contrib
deb-src http://ftp.jp.debian.org/debian/ buster-backports main contrib non-free
deb-src http://security.debian.org/debian-security buster/updates main
```

aptソースを編集したらupdateとしてupgradeします。

```
$ sudo apt-get update
$ sudo apt-get upgrade
```

# 基本的なコマンドと設定

シェルのエイリアスを設定します。定番どころを中心に設定して、場合によってはコメントアウトしておきます。

```
$ vi ~/.bashrc
```

```
alias ll='ls -l'
alias la='ls -A'
alias rm='rm -i'
alias mv='mv -i'
alias cp='cp -i'
alias vi='vim'
alias ..='cd ..'
```

設定ファイルを編集するのにvimをインストール。vimの設定は奥が深すぎていつも迷うので適当なところからスタートします。

```
$ sudo apt-get install vim
$ vi ~/.vimrc
```

```
set nocompatible
set encoding=utf-8
set fileencodings=utf-8,iso-2022-jp,sjis,euc-jp
set fileformats=unix,dos
set number
set list
set ruler
set autoindent
syntax on
highlight Comment ctermfg=LightCyan
set showmatch
set showcmd
set noswapfile
set nobackup
set history=50
set ignorecase
set smartcase
set hlsearch
set incsearch
set binary noeol
set tabstop=4
set expandtab
set shiftwidth=4
```

```
$ select-editor
```

ネットワーク内の端末とファイルを共有するためにsambaをインストールします。smb.confも適宜設定する。クライアントがWindows 10の場合はsambaのプロトコルを指定する必要があるみたい。SMB2以上じゃないと接続できない。

```
$ sudo apt-get install samba
$ sudo vi /etc/samba/smb.conf
```

```
unix charset = UTF-8
dos charset = CP932
display charset = UTF-8
interfaces = 127.0.0.0/8 192.168.0.0/24 eth0
client max protocol SMB3
client min protocol SMB2
[sharedfiles]
comment = server name here
path = /path/sharedfiles
writable = yes
public = no
guest ok = no
guest only = no
printable = no
force create mode = 0666
force directory mode = 0777
```

sambaのユーザに自分を追加してリスタートします。

```
$ sudo pdbedit -a YOUR_USER_NAME
$ sudo systemctl restart smbd
```

基本的なコマンドと言いながら、bashとvimとsambaだけだし。それしか必要ないってのが現状だし……。

# 録画関連コマンドのインストール

pt2を動かすドライバとカードリーダーの設定をさくっと済ませます。

```
$ sudo apt-get install \
    g++ \
    build-essential \
    autoconf \
    automake \
    cmake \
    linux-headers-`uname -r` \
    git \
    pcscd \
    pcsc-tools \
    libpcsclite-dev
```

pcsc_scanで動作確認しておきます。確認できたらCtr+C

```
$ pcsc_scan
```

b25コマンドはB-CASカードがリーダーから抜けていてデコードできなかったファイルをあとからデコードしたい時などに便利ですね。

```
$ mkdir downloads
$ cd downloads
$ git clone https://github.com/stz2012/libarib25.git
$ cd libarib25/
$ cmake .
$ make
$ sudo make install
```

earth_pt1というドライバがロードされているのでrmmodした上で、ブラックリストに登録します。

```
$ lsmod | grep pt1
$ sudo rmmod earth_pt1
$ sudo vi /etc/modprobe.d/blacklist.conf
```

```
blacklist earth_pt1
```

PT2を動作させるドライバーであるpt1_drvをインストールします。

```
$ wget http://hg.honeyplanet.jp/pt1/archive/tip.tar.bz2
$ tar xvf tip.tar.bz2
$ cd pt1-xxxx/driver/
$ make
$ sudo make install
$ sudo modprobe pt1_drv
$ lsmod | grep pt1
```

pt1_drvがロードされたのを確認したら録画コマンドrecpt1をインストールします。

```
$ cd ../recpt1/
$ ./autogen.sh
$ ./configure --enable-b25
$ make
$ sudo make install
$ ls -la /dev/pt1*
```

デバイスが確認できたらシグナル受信状況を確認したり、実際に録画してみます。

```
$ checksignal --device /dev/pt1video0 --lnb 15 211
$ checksignal --device /dev/pt1video1 --lnb 15 211
$ checksignal --device /dev/pt1video2 20
$ checksignal --device /dev/pt1video3 20
$ recpt1 --b25 --strip 20 10 test.ts
```

# MirakurunとEPGStationのインストール

はじめは全部まとめられたDockerで導入をしてみたのです。しかし、どういうプログラムなのかさっぱり理解せずに導入したので挙動がよくわからない。いろいろ不便。いまはDockerを利用せずに運用しています。ほかに何かを動かすわけでもないので見通しのよいようにします。

[Mirakurun][link-Mirakurun]をひとまず導入します。

Mirakurunはnode.js上で動作するので最新のnode.jsを取り入れつつインストールします。インストールスクリプトを信用しているのであまり小難しいことは考えずに実行。

```
$ sudo apt-get install libssl-dev libtool pkg-config yasm
$ npm install pm2 -g
$ curl -sL https://deb.nodesource.com/setup_12.x -o nodesource_setup.sh
$ sudo bash nodesource_setup.sh 
$ sudo apt install nodejs
```

node.jsのバージョンを確認しておきます。

```
$ node -v
```

必要だと言われているものをインストール。コマンドを実行します。

```
$ sudo npm install pm2 -g
$ sudo npm install arib-b25-stream-test -g --unsafe
$ sudo npm install mirakurun -g --unsafe --production
```

チューナーの名前をPT3からPT2にするのは識別名でしかないのでそのままでもよいはずが気分的に変更。デバイス名は正しく編集します。それとisDisabledはfalseにすることが大事です。ちなみに2枚のPT2で稼働させる時のチューナーの設定は次の通り。デバイスの番号がどう割り当てられるかってとカード単位なんですね。

```
$ sudo mirakurun config tuners
```

```
- name: PT2-S1
  types:
    - BS
    - CS
  command: recpt1 --device /dev/pt1video0 --lnb 15 <channel> - -
  decoder: arib-b25-stream-test
  isDisabled: false

- name: PT2-S2
  types:
    - BS
    - CS
  command: recpt1 --device /dev/pt1video1 --lnb 15 <channel> - -
  decoder: arib-b25-stream-test
  isDisabled: false

- name: PT2-T1
  types:
    - GR
  command: recpt1 --device /dev/pt1video2 <channel> - -
  decoder: arib-b25-stream-test
  isDisabled: false

- name: PT2-T2
  types:
    - GR
  command: recpt1 --device /dev/pt1video3 <channel> - -
  decoder: arib-b25-stream-test
  isDisabled: false

- name: PT1-S3
  types:
    - BS
    - CS
  command: recpt1 --device /dev/pt1video4 --lnb 15 <channel> - -
  decoder: arib-b25-stream-test
  isDisabled: false

- name: PT1-S4
  types:
    - BS
    - CS
  command: recpt1 --device /dev/pt1video5 --lnb 15 <channel> - -
  decoder: arib-b25-stream-test
  isDisabled: false

- name: PT1-T3
  types:
    - GR
  command: recpt1 --device /dev/pt1video6 <channel> - -
  decoder: arib-b25-stream-test
  isDisabled: false

- name: PT1-T4
  types:
    - GR
  command: recpt1 --device /dev/pt1video7 <channel> - -
  decoder: arib-b25-stream-test
  isDisabled: false
```

チャンネルも適宜設定します。チャンネルスキャンなんてしなくてもいいですし。放送が終了したチャンネルを設定してしまうとmirakurunがepgを取得しようとチューナーを始終占有することになりますので必要なものだけに絞る方が良いと思います。チャンネルの名前は設定上の呼称です。適宜EPGの名称に置きかわりますので適当でも大丈夫。

```
$ sudo mirakurun config channels
```

```
- name: MX
  type: GR
  channel: '20'

- name: tvk
  type: GR
  channel: '18'

- name: chiba
  type: GR
  channel: '30'

- name: saitama
  type: GR
  channel: '32'

- name: CX
  type: GR
  channel: '21'

- name: TBS
  type: GR
  channel: '22'

- name: TX
  type: GR
  channel: '23'

- name: EX
  type: GR
  channel: '24'

- name: NTV
  type: GR
  channel: '25'

- name: NHK E
  type: GR
  channel: '26'

- name: NHK G
  type: GR
  channel: '27'

- name: NHK BS1
  type: BS
  channel: BS15_0
  serviceId: 101

- name: NHK BS1 (sub)
  type: BS
  channel: BS15_0
  serviceId: 102

- name: NHK BSプレミアム
  type: BS
  channel: BS03_1
  serviceId: 103

- name: NHK BSプレミアム (sub)
  type: BS
  channel: BS03_1
  serviceId: 104

- name: BS日テレ
  type: BS
  channel: BS13_0
  serviceId: 141

- name: BS日テレ (sub)
  type: BS
  channel: BS13_0
  serviceId: 142

- name: BS朝日
  type: BS
  channel: BS01_0
  serviceId: 151

- name: BS朝日 (sub)
  type: BS
  channel: BS01_0
  serviceId: 152

- name: BS-TBS
  type: BS
  channel: BS01_1
  serviceId: 161

- name: BSジャパン
  type: BS
  channel: BS01_2
  serviceId: 171

- name: BSフジ
  type: BS
  channel: BS13_1
  serviceId: 181

- name: WOWOWプライム
  type: BS
  channel: BS03_0
  serviceId: 191
  isDisabled: false

- name: WOWOWライブ
  type: BS
  channel: BS05_0
  serviceId: 192
  isDisabled: false

- name: WOWOWシネマ
  type: BS
  channel: BS05_1
  serviceId: 193
  isDisabled: false

- name: スター・チャンネル1
  type: BS
  channel: BS09_1
  serviceId: 200
  isDisabled: false

- name: スター・チャンネル2
  type: BS
  channel: BS15_1
  serviceId: 201
  isDisabled: false

- name: スター・チャンネル3
  type: BS
  channel: BS15_1
  serviceId: 202
  isDisabled: false

- name: BS11
  type: BS
  channel: BS09_0
  serviceId: 211

- name: TwellV
  type: BS
  channel: BS09_2
  serviceId: 222

- name: 放送大学BS1
  type: BS
  channel: BS11_2
  serviceId: 231
  isDisabled: true

- name: 放送大学BS2
  type: BS
  channel: BS11_2
  serviceId: 232
  isDisabled: true

- name: 放送大学BS3
  type: BS
  channel: BS11_2
  serviceId: 233
  isDisabled: true

- name: グリーンチャンネル
  type: BS
  channel: BS19_0
  serviceId: 234
  isDisabled: true

- name: BSアニマックス
  type: BS
  channel: BS13_2
  serviceId: 236
  isDisabled: false

- name: FOXスポーツ＆エンターテイメント
  type: BS
  channel: BS11_0
  serviceId: 238
  isDisabled: true

- name: BSスカパー!
  type: BS
  channel: BS11_1
  serviceId: 241
  isDisabled: true

- name: J SPORTS 1
  type: BS
  channel: BS19_1
  serviceId: 242
  isDisabled: false

- name: J SPORTS 2
  type: BS
  channel: BS19_2
  serviceId: 243
  isDisabled: false

- name: J SPORTS 3
  type: BS
  channel: BS21_1
  serviceId: 244
  isDisabled: false

- name: J SPORTS 4
  type: BS
  channel: BS21_2
  serviceId: 245
  isDisabled: false

- name: BS釣りビジョン
  type: BS
  channel: BS23_0
  serviceId: 251
  isDisabled: true

- name: イマジカBS・映画
  type: BS
  channel: BS21_0
  serviceId: 252
  isDisabled: true

- name: 日本映画専門チャンネル
  type: BS
  channel: BS23_1
  serviceId: 255
  isDisabled: true

- name: ディズニー・チャンネル
  type: BS
  channel: BS03_2
  serviceId: 256
  isDisabled: true

- name: CS2
  type: CS
  channel: CS2

- name: CS4
  type: CS
  channel: CS4

- name: CS6
  type: CS
  channel: CS6

- name: CS8
  type: CS
  channel: CS8

- name: CS10
  type: CS
  channel: CS10

- name: CS12
  type: CS
  channel: CS12

- name: CS14
  type: CS
  channel: CS14

- name: CS16
  type: CS
  channel: CS16

- name: CS18
  type: CS
  channel: CS18

- name: CS20
  type: CS
  channel: CS20

- name: CS22
  type: CS
  channel: CS22

- name: CS24
  type: CS
  channel: CS24
```

ログのローテーションの設定も行っておきます。

```
$ sudo pm2 startup
$ sudo pm2 install pm2-logrotate
$ sudo vim /etc/logrotate.d/mirakurun
```

```
/usr/local/var/log/mirakurun.stdout.log
/usr/local/var/log/mirakurun.stderr.log
/{
  compress
  rotate 53
  missingok
  notifempty
}
```

EPGStationはデータベースを必要とします。今回はMySQL/mariaDBで構築します。

mariaDBをインストールしたら専用のデータベースを作成します。適宜データベースの名前やユーザは変更します。

```
$ sudo apt-get install mariadb-server
$ sudo mysql_secure_installation
$ sudo mysql -u root -p
> CREATE DATABASE epgstation CHARACTER SET utf8;
> GRANT ALL PRIVILEGES ON epgstation.* TO epgstation@localhost IDENTIFIED BY 'epgstation';
> ALTER USER epgstation@localhost IDENTIFIED BY 'epgstation';
> exit
```

ffmpegはソースからビルドするのが定番のようですが、パッケージでも十分ニーズを満たしているようなので簡単に済ませます。

```
$ sudo apt-get -s install ffmpeg
```

[EPGStation][link-EPGStation]のインストールもgithub上で公開されているとおりに実施。

```
$ git clone https://github.com/l3tnun/EPGStation.git
$ cd EPGStation
$ npm install --no-save
$ npm run build
```

設定ファイルはいろいろとありますが、ひとつずつ確認しながら編集します。

```
$ cp config/config.sample.json config/config.json
$ cp config/operatorLogConfig.sample.json config/operatorLogConfig.json
$ cp config/serviceLogConfig.sample.json config/serviceLogConfig.json
$ mkdir config/sample
$ mv config/*sample.json config/sample/
```

config.jsonはこのあたりは要編集ですね。ほかはおこのみ。

```
   "dbType": "mysql",
   "mysql": {
       "host": "localhost",
       "port": 3306,
       "user": "epgstation",
       "password": "epgstation",
       "database": "epgstation",
       "connectTimeout": 20000,
       "connectionLimit": 10
   },
   "ffmpeg": "/usr/bin/ffmpeg",
   "ffprobe": "/usr/bin/ffprobe",
```

さらに自動起動の設定をしておきます。

```
$ sudo npm install pm2 -g
$ sudo pm2 startup systemd -u YOUR_USER_NAME --hp /home/YOUR_USER_NAME
$ pm2 start dist/server/index.js --name "epgstation"
$ pm2 save
```

ここまで進めればひと段落なはず。ブラウザでポート8888にアクセスすればRPGStationのUIが表示されます。

# MirakurunとEPGStationの調整

基本的な調整は各種の設定ファイルに行っていきます。

まずMirakurunについて調整。tuners.ymlやchannels.ymlは追加の調整なし。server.ymlを調整します。

MirakurunとEPGStationの運用をはじめるとたびたび録画に失敗しました。どうやらEPGStationが録画を開始しようとすると空いているチューナーがない。つまりMirakurunがチューナーを占有してしまっている状態になっていると見受けられます。

```
programGCInterval: 86400000
epgGatheringInterval: 864000000
```

サーバーの設定のうちEPG取得のインターバルを変更します。EPG情報はEPGStaionが取得するのでMirakurunで取得する必要はありません。864000000ミリ秒＝10日にしておきます。ファイル末に追記。場合によってはMirakurun自体を修正してしまうこともありだと思います。

```
highWaterMark: 268435456
```

それとバッファの枯渇対策をちょっとだけしておきます。枯渇する前からやってしまうと正しいのかどうかちょっとわからなくなるので、必要に応じてでいいと思います。

しばらく運用してみましたが、デバイスが足りていないみたいであまり改善しませんでした。なので、物理的に解消することにします。

PT2は2枚持っているので2枚挿し。地デジ4チャンネルとBS/CS4チャンネルで運用することにしました。

設定はこのように変更。

```
highWaterMark: 268435456
programGCInterval: 43200000
epgGatheringInterval: 43200000
```

Mirakurunのログレベルなどほかの項目は変更せず様子を見ています。

EPGStationの調整箇所はconfig.jsonの部分。

```
    "recPriority": 2,
    "timeSpecifiedStartMargin": 5,
    "timeSpecifiedEndMargin": 1,
    "reservesUpdateIntervalTime": 720,
    "allowEndLack": true,
    "gid": "username",
    "uid": "username",
    "reservationAddedCommand": "/bin/bash /path/epgcommand.sh added",
    "recordedPreStartCommand": "/bin/bash /path/epgcommand.sh prestart",
    "recordedPrepRecFailedCommand": "/bin/bash /path/epgcommand.sh preprecfailed",
    "recordedStartCommand": "/bin/bash /path/epgcommand.sh start",
    "recordedEndCommand": "/bin/bash /path/epgcommand.sh end",
    "recordedFailedCommand": "/bin/bash /path/epgcommand.sh failed",
    "recordedFormat": "%TITLE%_%MONTH%%DAY%%HOUR%%MIN%%CHID%",
    "recorded": "/path/tsfiles/"
```

録画の開始と終了のマージンを少し増やしています。録画端末の環境により秒数は微妙に調整してあげるのが良いかと思います。コマンド立ち上げに要する時間が注目ポイントです。

EPGStationの実行ユーザやグループも変更します。外部のスクリプトを実行したりする時に権限やらをあれこれ考えていたら面倒なので自分にしてしまうのが楽かもしれません。また外部スクリプトを指定。引数で動作を変えるなど編集の利便性を考えます。

また録画ファイルの保存ディレクトリも場所を変えておきました。接続した大容量ハードディスクなどをマウントしておくと便利でしょう。

外部スクリプトでは環境変数もいくつか引き継がれています。録画開始をツイートしたり、録画のエラーをメールしたりなど柔軟な対応の余地があります。TSファイルを保存するディレクトリに録画状況を切り出したログの出力をして、いちいち正規のログを見なくて済むようにしていますが、悪くない利便性です。

```
#!/usr/bin/env bash

set -eu

SCRIPT_DIR=/path
LOG_FILE=$SCRIPT_DIR/record_scripts.log

case $1 in
    "added")
        # reservationAddedCommand
        echo "[INFO] `date "+%Y-%m-%d %T"` [EPG] タイマー ${NAME} at ${CHANNELNAME}" >> $LOG_FILE
        ;;
    "prestart")
        # recordedPreStartCommand
        echo "[INFO] `date "+%Y-%m-%d %T"` [EPG] ○録画/一時停止 ${NAME} at ${CHANNELNAME}" >> $LOG_FILE
        ;;
    "preprecfailed")
        # recordedPrepRecFailedCommand
        echo "[ERROR] `date "+%Y-%m-%d %T"` [EPG] 録画できません ${NAME} at ${CHANNELNAME}" >> $LOG_FILE
        ;;
    "start")
        # recordedStartCommand
        echo "[INFO] `date "+%Y-%m-%d %T"` [EPG] ●録画 ${NAME} at ${CHANNELNAME}" >> $LOG_FILE
        ;;
    "failed")
        # recordedFailedCommand
        echo "[ERROR] `date "+%Y-%m-%d %T"` [EPG] 録・画・失・敗 ${NAME} at ${CHANNELNAME}" >> $LOG_FILE
        ;;
    "end")
        # recordedEndCommand
        echo "[INFO] `date "+%Y-%m-%d %T"` [EPG] ■停止 ${NAME} at ${CHANNELNAME}" >> $LOG_FILE
        ;;
esac
```

連動して映画のx265エンコード自動化なんてのが便利でいいですね。ここからいろいろ追加していこうと思います。

# Docker上にtssplitter環境

TSファイルを編集するにはTsSplitter.exeはやっぱり便利です。wine32をDocker上で動作させます。DockerとDocker Composeをインストールしておきます。

```
$ sudo apt-get update
$ sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
$ curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
$ sudo apt-key fingerprint 0EBFCD88
$ sudo add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/debian \
    $(lsb_release -cs) \
    stable"
$ sudo apt-get update
$ sudo apt-get install docker-ce docker-ce-cli containerd.io
$ sudo docker run hello-world
$ sudo curl -L "https://github.com/docker/compose/releases/download/1.25.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
$ sudo chmod +x /usr/local/bin/docker-compose
```

以上でDockerの導入が完了。

TsSplitterはバイナリを入手した上でDockerfileを編集しビルドします。

```
FROM debian:buster

ENV WINEDEBUG -all
ENV LANGUAGE ja_JP.ja \
  LANG ja_JP.UTF-8 \
  LC_ALL ja_JP.UTF-8

RUN dpkg --add-architecture i386 \
  && apt-get update \
  && apt-get install -y --no-install-recommends \
  wine \
  wine32 \
  wine64 \
  wine32:i386 \
  libwine \
  libwine:i386 \
  fonts-wine \
  locales \
  && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
  && echo "ja_JP.UTF-8 UTF-8" >> /etc/locale.gen \
  && locale-gen \
  && apt-get autoremove -y \
  && apt-get clean

RUN useradd -u 1000 -d /home/YOUR_USER_NAME -m -s /bin/bash YOUR_USER_NAME
ENV HOME /home/YOUR_USER_NAME
WORKDIR /home/YOUR_USER_NAME
USER YOUR_USER_NAME
RUN winecfg
COPY ./TsSplitter.exe /usr/local/bin/
VOLUME /home/YOUR_USER_NAME/videos/ex2TBHDD/recorded
ENTRYPOINT [ "/usr/bin/wine" ]
```

ビルドします。

```
$ sudo docker build -t wine32 ~/tssplitter/.
```

こんな記法で利用できます。

```
$ sudo docker run --rm --mount type=bind,src=$PWD,dst=$PWD wine32 /usr/local/bin/TsSplitter.exe -SD -1SEG -SEP -SEPA "$PWD/source.ts"
```

# 運用に便利なシェルスクリプトを用意する

適宜、スクリプトに連動させて動かします。wowowのような5.1chの映画なんかはTsSplitterを通すだけで切り抜きできますから重宝しています。

tsの編集に追加して、エンコードするコマンドを追加。

```
$ sudo apt-get install handbrake-cli
```

当初はDockerの中で動かしていましたが、あまり意味がないのでそのままインストールしているHandbrake-CLI。ffmpegよりもこちらの方が使い慣れているのでh265のファイル生成なんかに使っています。

ある程度環境が落ち着いてきたので、エンコードスクリプトの整備を進めました。

まずはconfig.jsonの編集

```
    "encode": [
        {
            "name": "wowow 5.1ch",
            "cmd": "/bin/bash %ROOT%/config/wowow.sh",
            "suffix": ".mp4"
        },
        {
            "name": "H265",
            "cmd": "/bin/bash %ROOT%/config/handbrake.sh h265-med-28",
            "suffix": "-265.mp4"
        },
        {
            "name": "H264",
            "cmd": "/bin/bash %ROOT%/config/handbrake.sh h264-med-23",
            "suffix": "-264.mp4"
        },
        {
            "name": "H264 veryfast",
            "cmd": "%NODE% %ROOT%/config/enc.js",
            "suffix": "-vf.mp4",
            "default": true
        }
    ],
```

エンコードのメニューとして「wowow 5.1ch」、「H265」、「H264」、「H264 veryfast」としました。「H264 veryfast」は手早くエンコードするときのため。初期のものをそのまま残しています。慣れの問題で基本的なエンコードはHandbrakeCLIで実施します。古いデバイスを考慮してのH264とここ数年のものなら問題ないH265でエンコードするためにひとつ。内容は次の通り。

```
#!/usr/bin/env bash

set -eux

SCRIPT_DIR=/path
LOG_FILE=$SCRIPT_DIR/record_scripts.log

case $1 in
    "h265-med-28")
        ENCSTRING="-e x265 --x265-preset=medium --h265-profile=main -q 28"
        ;;
    "qsv_h265-med-28")
        ENCSTRING="-e qsv_h265 --x265-preset=medium --h265-profile=main -q 28"
        # QSVはあまり効果がないかも
        ;;
    "h264-med-23")
        ENCSTRING="-e x264 --x264-preset=medium --h264-profile=main -q 23"
        ;;
    "qsv_h264-med-23")
        ENCSTRING="-e qsv_h264 --x264-preset=medium --h264-profile=main -q 23"
        # QSVはあまり効果がないかも
        ;;
    "h264-veryfast-23")
        ENCSTRING="-e x264 --x264-preset=veryfast --h264-profile=main -q 23"
        # QSVはあまり効果がないかも
        ;;
    "")
        ENCSTRING="-e h264 --x264-preset=veryfast --h264-profile=main -q 23"
        ;;
esac

echo "[INFO] `date "+%Y-%m-%d %T"` [handbrake] ●REC ${OUTPUT##*/}" >> $LOG_FILE

/usr/bin/HandBrakeCLI \
    -f mp4 $ENCSTRING --detelecine -l 720 --crop 0:0:0:0 \
    --aencoder copy:aac --mixdown auto \
    -i "$INPUT" \
    -o "$OUTPUT" 1> /dev/null

echo "[INFO] `date "+%Y-%m-%d %T"` [handbrake] ■STOP ${OUTPUT##*/}" >> $LOG_FILE
```

特にファイル名を変更したりとか考えず、入力されたファイルを指定したコーデックとプリセットでエンコードします。QSVの設定も書いてみましたが多少早くなったとしても画質の損失がそれに見合わないと感じたので使っていません。

次にwowowなどの5.1chソースの動画をエンコードするスクリプト。TsSplitterで音声チャンネルの切り替えで動画をカットすると本編部分だけの動画が切り出せるので、それをエンコードするようにシェルスクリプトを書いています。

```
#!/usr/bin/env bash

set -eux

SCRIPT_DIR=/path
LOG_FILE=$SCRIPT_DIR/recorder.log

WORK_DIR=${INPUT%/*}
INPUT_FILE=${INPUT##*/}
OUTPUT_FILE=${OUTPUT##*/}

TASK_NO=`date "+%H%M"`

sleep 1m

echo "[INFO] `date "+%Y-%m-%d %T"` [tsspliter] ●START $INPUT_FILE" >> $LOG_FILE
cd $WORK_DIR
splittemp=${TASK_NO}_split.ts
mv "$INPUT" "$WORK_DIR/$splittemp"
docker run --rm --mount type=bind,src=$WORK_DIR,dst=$WORK_DIR wine32 /usr/local/bin/TsSplitter.exe -SD -1SEG -SEP -SEPA "$WORK_DIR/$splittemp" 2>>$LOG_FILE
echo "[INFO] `date "+%Y-%m-%d %T"` [tsspliter] ■STOP $INPUT_FILE" >> $LOG_FILE        
i=0
for deletes in $( ls -S $WORK_DIR/${splittemp%.ts}_*.ts )
do
    if [ $i -eq 0 ]; then
        echo "[INFO] `date "+%Y-%m-%d %T"` [tsspliter] split $INPUT_FILE" >> $LOG_FILE
        encodetemp=${TASK_NO}_encode.ts
        mv $deletes $encodetemp
        i=1
    else
        echo "[INFO] `date "+%Y-%m-%d %T"` [tsspliter] remove $deletes" >> $LOG_FILE
        rm $deletes
    fi
done

echo "[INFO] `date "+%Y-%m-%d %T"` [handbrake] ●REC $INPUT_FILE" >> $LOG_FILE
ENCSTRING="-e x265 --x265-preset=medium --h265-profile=main -q 28"
#ENCSTRING="-e qsv_h264 --x264-preset=veryfast --h264-profile=main -q 23"
/usr/bin/HandBrakeCLI \
    -f mp4 $ENCSTRING --detelecine -l 720 --crop 0:0:0:0 \
    --aencoder copy:aac --mixdown auto \
    -i "$WORK_DIR/$encodetemp" \
    -o "$OUTPUT" 1> /dev/null
echo "[INFO] `date "+%Y-%m-%d %T"` [handbrake] ■STOP $OUTPUT_FILE" >> $LOG_FILE

mv "$WORK_DIR/$splittemp" "$INPUT"
mv "$WORK_DIR/$encodetemp" "${INPUT%.ts}-src.ts"
```

素人スクリプトなのでとっても冗長的です。上から簡単に解説します。

INPUTとOUTPUTはEPGStationから渡されるのでパスやファイル名を変数に格納。

作業に取り掛かる前に1分スリープしています。ファイル名を変更して作業するので録画直後に動作させてしまうとサムネイルの作成に失敗してしまいますので猶予をもたせています。

作業時のファイル名は時間を付与して重複するのを回避しています。

TsSplitterで分割したらファイルサイズでソートして大きなものをエンコード対象ファイルとして小さなものは削除します。

エンコードはH265で標準的なプリセットに設定。やっぱり標準がいちばんバランスいいと思います。

作業が終わったら元動画の名称を戻します。元動画、余分な部分を削除した動画、エンコードした動画の3つになります。頻繁にスクリプトを調整していますが、ここのところは安定傾向です。

それと過去に録画したTSファイルをH265に再度エンコードするスクリプトも用意しました。EPGStationのエンコードを圧迫しないようにプロセスを確認してから動作するようにしてます。H264のライブラリをH265にしてホームサーバのディスク容量を節約しているつもりです。

```
#!/usr/bin/env bash

set -eux

SCRIPT_DIR=/home/koichiroyamada/record_scripts
LOG_FILE=$SCRIPT_DIR/recorder.log

STOCK_DIR=ウルトラマン
SOURCE_DIR=/path/$STOCK_DIR
OUTPUT_DIR=/path/enc/$STOCK_DIR

TASK_NO=`date "+%H%M"`

PROCESS_NAME="265.sh"
count=`ps -ef | grep $PROCESS_NAME | grep -v grep | wc -l`
echo "[INFO] `date "+%Y-%m-%d %T"` [x265][$TASK_NO] script awake" >> $LOG_FILE
if [ $count -lt 4 ]; then
    echo "[INFO] `date "+%Y-%m-%d %T"` [x265][$TASK_NO] ... no processes exist ($count)" >> $LOG_FILE
else
    echo "[INFO] `date "+%Y-%m-%d %T"` [x265][$TASK_NO] ... another process still working ($count)" >> $LOG_FILE
    echo "[INFO] `date "+%Y-%m-%d %T"` [x265][$TASK_NO] script dismiss" >> $LOG_FILE
    exit 1
fi

if ls $SOURCE_DIR/*.ts >/dev/null 2>&1; then
    cd $SOURCE_DIR
    IFS_BACK="$IFS"
    IFS=$'\n'
    for target in $(ls -1 $SOURCE_DIR/*.ts)
    do
        target_file="${target##*/}"
        if [ -s "$OUTPUT_DIR/${target_file%.ts}.mp4" ]; then
            echo "[INFO] `date "+%Y-%m-%d %T"` [x265][$TASK_NO] skip ${target_file%.ts}.mp4" >> $LOG_FILE
        else
            PROCESS_NAME="TsSplitter.exe"
            count=`ps -ef | grep $PROCESS_NAME | grep -v grep | wc -l`
            if [ $count -lt 1 ]; then
                echo "[INFO] `date "+%Y-%m-%d %T"` [x265][$TASK_NO] split process clean ($count)" >> $LOG_FILE
            else
                echo "[INFO] `date "+%Y-%m-%d %T"` [x265][$TASK_NO] ... another split process found" >> $LOG_FILE
                echo "[INFO] `date "+%Y-%m-%d %T"` [x265][$TASK_NO] script dismiss" >> $LOG_FILE
                exit 1
            fi
            PROCESS_NAME="HandBrakeCLI"
            count=`ps -ef | grep $PROCESS_NAME | grep -v grep | wc -l`
            if [ $count -lt 1 ]; then
                echo "[INFO] `date "+%Y-%m-%d %T"` [x265][$TASK_NO] encode process clean ($count)" >> $LOG_FILE
            else
                echo "[INFO] `date "+%Y-%m-%d %T"` [x265][$TASK_NO] ... another encode process found" >> $LOG_FILE
                echo "[INFO] `date "+%Y-%m-%d %T"` [x265][$TASK_NO] script dismiss" >> $LOG_FILE
                exit 1
            fi
            echo "[INFO] `date "+%Y-%m-%d %T"` [x265][$TASK_NO] ●REC ${target_file%.ts}.mp4" >> $LOG_FILE
            /usr/bin/HandBrakeCLI -f mp4 -l 720 --crop 0:0:0:0 \
                -e x265 --x265-preset=medium --h265-profile=main -q 28 --detelecine \
                --aencoder copy:aac --mixdown auto \
                -i "$SOURCE_DIR/$target_file" \
                -o "$OUTPUT_DIR/${target_file%.ts}.mp4" 1> /dev/null
            echo "[INFO] `date "+%Y-%m-%d %T"` [x265][$TASK_NO] ■STOP ${target_file%.ts}.mp4" >> $LOG_FILE
        fi
    done
    IFS="$IFS_BACK"
else
    echo "[INFO] `date "+%Y-%m-%d %T"` [x265][$TASK_NO] ... no files to encode" >> $LOG_FILE
fi
echo "[INFO] `date "+%Y-%m-%d %T"` [x265][$TASK_NO] script dismiss" >> $LOG_FILE

```

crontabで定時で起動するスクリプトにしました。自身がすでに稼働していたら終了。また、先のwowow用スクリプトを念頭にTsSplitterやHandbrakeが起動していたら動作を終了します。何もしていなかったら指定したフォルダのTSファイルをH265に順次エンコードするというのがおおまかな動作内容です。

もっとスマートなやり方があると思いますが、動きゃいいんだよでそのままです。とても安定しておりますね。

いまのところ、こんな感じで動作していますが、環境によってはFirewallなんかもあわせて設定する必要があるでしょうね。
