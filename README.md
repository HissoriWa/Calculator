# Calculator-v1.0

>[!Important] 
## Credit
本アプリは、[JXMai氏のCalculator](https://github.com/JiXiaomai/SMM2Calculator)をスマートフォンやその他の媒体で利用可能にするための移植を主な目的として作成されたものです。したがって、本アプリの設計・アルゴリズム等は**JXMai氏のものを非常に参考にしています。**
そのため、著作権的な問題あるいは本人からの申し立てがあった場合には、ただちに公開を停止いたします。　

---

## How to Use

### Calculateモード
操作やそのほかの条件を指定し、マリオの座標変化を調べます。針に当たったかどうかの判定も可能です。
### Find Setupsモード(実験的)
初期位置と目的地のx座標を指定し、マリオが4種類の地面移動(左右+Y有無)と3種類の減速(立ち、前後しゃがみ)で目的地に到達できる操作を探索します。
SubpixelがOnのときはサブピクセルパーフェクト、そうでなければ針の左右と同じ猶予を許します。

上にある機能から順番に説明しています。わからないものは読んでください。
<dl>
<dt>Input/Get as hex</dt>
<dd>x Pos, x Spd, y Pos, y Spd, 計算結果を16進数で設定・表示できます。</dd>
<dt>x Pos, x Spd, y Pos, y Spd</dt>
<dd>マリオの座標です。1 Block = 16とする単位です。</dd>
<dt>Width, Height</dt>
<dd>画面のブロック数です。あまり大きいと縮小表示されます(streamlit側の仕様)。</dd>
<dt>Skin, BackGround</dt>
<dd>見た目を指定できます。適当に作ったのでこれはあまり信頼しないでください。</dd>
<dt>Condition</dt>
<dd>夜雪、夜空、スターなど状態異常を設定できます(夜砂漠=Windは適当に作ったので、これも信頼しないでください)。</dd>
<dt>Trail, Duck</dt>
<dd>TrailがOnのときは、操作の切り替えの時以外もマリオの軌跡が薄く表示されます。DuckがOnのときは常にしゃがみます。</dd>
<dt>Setups, Load the Setup</dt>
<dd>あらかじめ用意されたセットアップのロードができます。隣のAdd...などは制作に用いただけなので無視してください。</dd>
<dt>Enter in JXMai Format</dt>
<dd>Onのとき、JXMai氏のCalculatorと同じフォーマットでCommandsの入力が可能です(こちらが追加していない操作は使えません)。</dd>
<dt>Commands</dt>
<dd>決められたフォーマットで入力後、Calculateを押すことで結果が表示されます。</dd>
<dt>Calculate!</dt>
<dd>結果(最終x, y座標・速度と針に当たったかどうか)を表示します。</dd>
<dt>Spike Positionやその周辺</dt>
<dd>Spike Positionに追加・撤去したい針・地面の座標(x, yの順。画面の白文字が座標)を入力し、Add/Erace Spikes/Groundsを押し、Calculate!を実行するとその地点の針・地面が追加・撤去できます。Erace All...ですべて(Groundsは初期除き)消せます。x y x y ...のように同時に複数個の針を指定できます。</dd>

>Find Setupsモード
<dt>Target point</dt>
<dd>目標地点のx座標です。</dd>
<dt>Difficulty</dt>
<dd>操作の切り替え回数です。大きいほど処理が重くなります。</dd>
<dt>Lim Frames</dt>
<dd>*方向キーを押しているフレーム数の最大*です。大きいほど処理が重くなります。</dd>
<dt>Search!</dt>
<dd>探索を実行します。処理能力が低いため、動かなくなることが多いです。</dd>
