# Calculator-v1.0

[!Important] 
## Credit
本アプリは、[JXMai氏のCalculator](https://github.com/JiXiaomai/SMM2Calculator)をスマートフォンやその他の媒体で利用可能にするための移植を主な目的として作成されたものです。したがって、本アプリの設計・アルゴリズム等は**JXMai氏のものを非常に参考にしています。**
そのため、著作権的な問題あるいは本人からの申し立てがあった場合には、ただちに公開を停止いたします。　

---

## How to Use
上にあるから順番に説明します。わからないものは読んでください。
<dl>
<dt>Input/Get as hex</dt>
<dd>x Pos, x Spd, y Pos, y Spd, 計算結果を16進数で設定・表示できます。</dd>
<dt>x Pos, x Spd, y Pos, y Spd</dt>
<dd>マリオの座標です。**1 Block = 16**とする単位です。</dd>
<dt>Width, Height</dt>
<dd>画面のブロック数です。あまり大きいと縮小表示されます(streamlit側の仕様)。</dd>
<dt>Trail, Duck</dt>
<dd>TrailがOnのときは、操作の切り替えの時以外もマリオの軌跡が薄く表示されます。DuckがOnのときは常にしゃがみます。</dd>
<dt>Setups, Load the Setup</dt>
<dd>あらかじめ用意されたセットアップのロードができます。隣のAdd...などは制作に用いただけなので無視してください。</dd>
<dt>Enter in JXMai Format</dt>
<dd>Onのとき、JXMai氏のCalculatorと同じフォーマットで入力が可能です(こちらが追加していない操作は使えません)。</dd>
<dt>Commands</dt>
<dd>決められたフォーマットで入力後、Calculateを押すことで結果が表示されます。</dd>
<dt>Calculate!</dt>
<dd>結果(最終x, y座標・速度と針に当たったかどうか)を表示します。</dd>
<dd>Spike Positionやその周辺</dd>
<dt>Spike Positionに追加・撤去したい針・地面の座標(x, yの順。画面の白文字が座標)を入力し、Add/Erace Spikes/Groundsを押し、Calculate!を実行するとその地点の針・地面が追加・撤去できます。Erace All...ですべて(Groundsは初期除き)消せます。x y x y ...のように同時に複数個の針を指定できます。</dt>
<dt></dt>
