# ディスプレイアーム モーター操作用Socket.io

Socket.IOを使って通信する

- client → RasPi

    http://${IPADDR}:5000/motor

- RasPi → client

    http://${IPADDR}:5000/

## モーターフェッチ開始

モーター情報の取得を開始する。

このタイミングでモーターとRasPiが接続されていなければ接続する

スマホから操作する際は必ずこの処理を実行すること

**イベント名**

enable_fetch_motor

**接続例(Node.js)**

```
import io from 'socket.io-client'

const socket = io(`${SOCKET_IO_URL}`)
socket.emit("enable_fetch_motor")
```

## モーター角度操作

モーターの角度を操作する

フィギュア／プラモデルの姿勢制御に使う

**イベント名**

rotate

**接続例(Node.js)**

```
import io from 'socket.io-client'

const socket = io(`${SOCKET_IO_URL}`)
socket.emit("rotate", {"id" : id /* "motor1", "motor2" or "motor3" */,
                       "rad" : rad /* deg * PI / 180 */})
```

## モーター角度初期化**

現在のモータの角度を0度として設定する。

関節の曲がり過ぎによる事故を防ぐために必要

**イベント名**

init_pos

**接続例**

```
import io from 'socket.io-client'

const socket = io(`${SOCKET_IO_URL}`)
socket.emit("init_pos")
```
