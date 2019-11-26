---
title: Gradient Descent（勾配降下法）
layout: notebook
toc: true
published: 2019-11-25
last_edit: 2019-11-25
---

```python
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
plt.rcParams["figure.figsize"] = (10,8)
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['Noto Sans CJK JP']
from IPython.display import HTML
import csv
```

[前回](./linear-regression.html)では、線形回帰とはどういうものかについて考え、線形回帰の解析的な解き方ー数式を変形して計算するーで解くことを学びました。**正規方程式**を定義し、それを解いて回帰線の式を得たわけですが、正規方程式では重要な問題が2つあると述べました。逆行列が求めにくいのと、計算の制度が落ちるという理由で、正規方程式が実はあまり使われないと述べました。

となると、ではどのような方法で解ければいいでしょうか。この問の答えになってくれるのが**Gradient Descent**（勾配降下法）です。

# 関数の最適化

まずは簡単な問題から始めましょう。ある関数$y = f(x)$の最小値を知りたい時、どうやって求めればいいでしょうか。当然答えは、$y\prime = 0$と起き、それを満たす$x$を探すわけです。これを**解析的**アプローチと言います。しかし、前回述べたように、解析的に中々解きにくい問題もあります。なので、今度は$y\prime = 0$を解くことを禁止して、別の方法で最小値を探す方法を考えなければなりません。

一つの方法は、あらゆる$x$の値全てに対し$y$を計算し、その中から最小値とその$x$値を選ぶというやり方です。しかし、ご存知のように実数は無限なので、それも中々難しいです。一方、パソコンで表現できる実数は約$2^{64} = 18446744073709551616$通りあるのですが、それら全部を試してみるのを考えると、1秒に1000000000個（そもそも無理）試せたとしても600年ぐらいかかります。というわけで値を全部試すことは無理なので、$x$を賢く選んで、試す値の個数を最低限に抑える方法を探さなければいけません。

ではどうやって$x$の値を選べば良いでしょうか。答えは、「隣の$x$」を見ることです。左隣（負の方向）の$x_l$での$y_l$が自分より大きければ、左（負の方向）に行く必要がありません。一方右隣（正の方向）の$x_r$での$y_r$が自分より小さければ、右（正の方向）に行くと最小値に近づくことになります。しかし残念ながら、この方法も一つ落とし穴があります。皆さんは既に気づいているかもしれませんが、極小値（グラフでの谷）が何個もあると、その中の一つにたどり着いたらそこからもう抜け出すことができません（右も左も自分より大きいので）。これを数学の言葉で言うと、$f(x)$が[Convex Function](https://ja.wikipedia.org/wiki/%E5%87%B8%E9%96%A2%E6%95%B0)（凸関数）の時のみこの方法が最小値を出すことが保証されます。

これ以上賢いことを考えようとすると、話が複雑になるので、今回は最適化したい関数が凸関数であると仮定し、隣を見る方法について解説します。

# 隣を見る

上では「隣の$x$での$y$を見る」と書きましたが、集合に詳しい人は「実数の集合で隣の$x$なんて概念はないよ！」と、心の中で叫んでるはずです。その通りです。$\pi$の隣の数なんてのは定義できないので、数学を語る時は別の捉え方をする必要があります。

良く考えてみると、「隣を見る」時のパターンは4通りあります。一つは、左が小さく、右が大きいパターン。もう一つは、左が大きく、右が小さいパターン。そして残りの2つは、左も右もともに小さい、もしくは大きいパターン。ここまで言うともう分かると思うのですが、「隣を見る」というのは実は微分で表すことができます！微分は関数の変化の激しさを表してくれるので、負の時は1つめのパターン、正の時は2つめのパターン、0の時は3つ目と4つ目のパターンに対応します。

これを図で表すと、以下のようなイメージです。


```python
x = np.linspace(-10, 10, 100) # -10から10までの点を等間隔で100個生成
y = x ** 2
fig, ax = plt.subplots(1, 1)
ax.plot(x, y) # 点を通った線を描く
vx = np.linspace(-10, 10, 20)
ax.quiver(vx, vx ** 2, 2 * vx, np.zeros_like(vx), headwidth=4, width=0.005, scale=200) # ベクトル場（矢印）を描く
```




    <matplotlib.quiver.Quiver at 0x7fe90fe00590>




![png](gradient-descent_files/gradient-descent_6_1.png)


この図では、微分関数の値が負の時に矢印が左を指し、正の時は右を指します。そして矢印の長さは、微分関数の絶対値に比例します。みての通り、微分はどこに行けば増加するか、そしてどれぐらい増加するかを教えてくれます。もちろん、最小値（谷の底）では微分がゼロ（に近い）ので、矢印の長さが0になっています。

# 微分を使って最適化する

上の話をまとめましょう。まず、関数$f(x)$の微分関数$\frac{df}{dx}$は**増加方向**と**増加程度**を教えてくれます。これを最小値の探索にどう使うのかというと、現在見ている$x_1$からその$x_1$での微分関数の値を引き算すれば良いです。そうすると、どこか新しい$x_2$に辿り着くことができ、その$x_2$に対し$f\prime(x_2) \leq f\prime(x_1)$が成り立ちます。この操作を何回も繰り返せば、微分値がどんどん小さくなっていき、無限回繰り返すと微分値が0に収束します。

しかし、これだけでは不十分です。例えば、$f(x) = x^2$を考えます。この時上の過程を5回繰り返し、辿った$x$を出力してみましょう。最初値は$x=0$で得られるので、そこに近づいていけば正しい動作です。


```python
xs = [-8.0]
print("x_0 =", xs[0])
for i in range(5):
    dfdx = 2 * xs[i]
    xs.append(xs[i] - dfdx)
    print(f"x_{i + 1} = x_{i+1} - f'(x_{i+1}) = ({xs[i]:+}) - ({dfdx:+}) = {xs[i+1]:+}")
```

    x_0 = -8.0
    x_1 = x_1 - f'(x_1) = (-8.0) - (-16.0) = +8.0
    x_2 = x_2 - f'(x_2) = (+8.0) - (+16.0) = -8.0
    x_3 = x_3 - f'(x_3) = (-8.0) - (-16.0) = +8.0
    x_4 = x_4 - f'(x_4) = (+8.0) - (+16.0) = -8.0
    x_5 = x_5 - f'(x_5) = (-8.0) - (-16.0) = +8.0


$f\prime(x) = 2x$なので、同じ二つの$x$値を交互に辿っているだけです。全く話になりません。

では、$f(x) = 10x^2$はどうなるでしょうか。同じく最小値は$x=0$で得られます。


```python
xs = [-8.0]
print("x_0 =", xs[0])
for i in range(5):
    dfdx = 2 * 10 * xs[i]
    xs.append(xs[i] - dfdx)
    print(f"x_{i + 1} = x_{i+1} - f'(x_{i+1}) = ({xs[i]:+}) - ({dfdx:+}) = {xs[i+1]:+}")
```

    x_0 = -8.0
    x_1 = x_1 - f'(x_1) = (-8.0) - (-160.0) = +152.0
    x_2 = x_2 - f'(x_2) = (+152.0) - (+3040.0) = -2888.0
    x_3 = x_3 - f'(x_3) = (-2888.0) - (-57760.0) = +54872.0
    x_4 = x_4 - f'(x_4) = (+54872.0) - (+1097440.0) = -1042568.0
    x_5 = x_5 - f'(x_5) = (-1042568.0) - (-20851360.0) = +19808792.0


最小値に辿り着くどころか、どんどん遠ざかっていってます。どういうことかというと、$f\prime(x_i) = f\prime(-x_i)$なので、もし$|x_{i+1}| > |x_i|$になったら、微分値が前より大きくなり、それが繰り返し起こると$x_i$が発散します。（各自図を描いてみて確認しましょう）

というわけで、微分を引くだけだと、$x$が発散したり、二つの値を往復したりしてしまうことになりえるので、何か工夫をしなければいけません。ここで一番簡単な解決策は、微分値を引く前に係数をかけることです。この係数を$\alpha$だとして、$\alpha$が小さければ小さいほど、$x$が動く「歩幅」が小さくなるので、この二つの問題を防ぐことができます。

改めて$f(x) = 10x^2$の最小値を探してみましょう。今回は、$\alpha = 0.04$に設定しておきます。


```python
xs = [-8.0]
alpha = 0.04
print("x_0 =", xs[0])
for i in range(5):
    dfdx = alpha * 2 * 10 * xs[i]
    xs.append(xs[i] - dfdx)
    print(f"x_{i + 1} = x_{i+1} - f'(x_{i+1}) = ({xs[i]:+.3f}) - ({dfdx:+.3f}) = {xs[i+1]:+.3f}")
```

    x_0 = -8.0
    x_1 = x_1 - f'(x_1) = (-8.000) - (-6.400) = -1.600
    x_2 = x_2 - f'(x_2) = (-1.600) - (-1.280) = -0.320
    x_3 = x_3 - f'(x_3) = (-0.320) - (-0.256) = -0.064
    x_4 = x_4 - f'(x_4) = (-0.064) - (-0.051) = -0.013
    x_5 = x_5 - f'(x_5) = (-0.013) - (-0.010) = -0.003


今回はちゃんと収束しますね！残念ながら、$\alpha$の値は最適化したい関数毎に自分で決めなければいけないです。注意しなければいけないのは、大きすぎると発散が起こり、小さすぎると収束に時間がかかります。

上手な決め方についてはまた今度書きますが、一旦は自分で試してみて、収束するようになるまで小さくしていくという決め方を使いましょう。

# 多次元に一般化する

今までは、1次元関数（変数が一つだけの関数）を最適化しました。しかし、機械学習や深層学習では、次元（変数）がいくらでもあります。線形回帰の場合はまだ10次元以内に収まるかもしれませんが、画像認識になるとピクセル数分の次元（数十万〜数千万）もありえます。しかし、いきなり数千万次元の関数を最適化しろと言われても無理があるので、これからは2次元関数の最適化について解説していきます。

## 多次元での微分

一次元での微分値$f\prime(x_1)$は、$x_1$をどの方向にずらせば$f(x_1)$が大きくなるか、そしてどれぐらい大きくなるかを教えてくれます。2次元になると、動かす物が2個--$x$と$y$--あるので、「どの方向に動かせばいいか」というのは自然とベクトルになります。そして、そのベクトルの絶対値が「どれぐらい大きくなるか」を教えてくれます。

では、このベクトルに何を入れればいいかというと、一つ目の要素には「$x$を動かすとどれぐらい大きくなるか」、もう一つの要素には「$y$を動かすとどれぐらい大きくなるか」を入れれば良いです。方向は符号で決まるのでもちろんそれぞれの符号も必要です。そして、この「◯を動かせば」という制約があるので、ここで偏微分が登場します。

さて、説明はここまでにして、話を数学の言葉に直しましょう。上で言ったベクトルは、**Gradient**（勾配）と言います。そしてその定義は以下です。

$$
\nabla f(x, y, z, ...) = \begin{pmatrix}
\frac{\partial f}{\partial x} \\
\frac{\partial f}{\partial y} \\
\frac{\partial f}{\partial z} \\
...
\end{pmatrix}
$$

ここで一つ注意点を述べましょう。関数が$f(x)$の時、つまり1次元関数である時、勾配は$x$での微分と等しいです。つまり：

$$
\nabla f(x) = \frac{df}{dx}
$$

## 勾配で関数を最適化する

勾配の意味をわかりやすくするために、関数$f(x, y) = x^2 + y^2$を考えましょう。この関数のグラフを描くと、以下の曲面ができます。


```python
r = np.linspace(-10, 10, 100)
xx, yy = np.meshgrid(r, r)
zz = xx ** 2 + yy ** 2
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot_surface(xx, yy, zz) # 曲面を描く
```




    <mpl_toolkits.mplot3d.art3d.Poly3DCollection at 0x7fe90f2b6c90>




![png](gradient-descent_files/gradient-descent_20_1.png)


次に、$f$の勾配を2次平面上に描くとどうなるのでしょうか。勾配の矢印が関数の高いところを指していることを意識して、次の図を描いてみましょう。


```python
r = np.linspace(-10, 10, 100)
xx, yy = np.meshgrid(r, r)
zz = xx ** 2 + yy ** 2
fig = plt.figure()
ax = fig.add_subplot()
c = ax.contourf(xx, yy, zz, levels=100) # 色付き等高線図を描く
fig.colorbar(c)

vr = np.linspace(-10, 10, 21)
vx, vy = np.meshgrid(vr, vr)
dfdx = 2 * vx
dfdy = 2 * vy
ax.quiver(vx, vy, dfdx, dfdy, color='white') # ベクトル場（勾配）を描く
```




    <matplotlib.quiver.Quiver at 0x7fe90c5c3510>




![png](gradient-descent_files/gradient-descent_22_1.png)


ここで、色は曲面の$z$座標 - $f(x, y)$の値 - を表します。みての通り、$(0, 0$で関数が最小値をとるので、勾配がゼロになるし、そこから遠ざかっていくとどんどん増加が激しくなり、矢印が長くなっていきます。

では、この関数を最適化するにはどうしたら良いのかというと、１次元の時と全く同じです。ただ今回は、$x_i$の変わりに$(x_i, y_i)$ベクトルから勾配ベクトルを引き、更新していきます。つまり：

$$
\begin{pmatrix}
x_{i+1} \\
y_{i+1}
\end{pmatrix} =
\mathbf{v}_{i+1}
= \mathbf{v} - \alpha\nabla f(x_i, y_i)
$$

さて、$f(x, y) = 2x^2 + y^2$を最適化してみましょう。$\alpha$を$0.1$と置いて、10回計算していきます。


```python
v = np.array([-5.0, -8.0])
vs = [v] # vの履歴
alpha = 0.1
print(f"v_0 =", v)
for i in range(10):
    v = v - alpha * np.array([ 4 * v[0], 2 * v[1] ]) # vの更新
    vs.append(v)
    print(f"v_{i+1} =", v)
vs = np.array(vs)
```

    v_0 = [-5. -8.]
    v_1 = [-3.  -6.4]
    v_2 = [-1.8  -5.12]
    v_3 = [-1.08  -4.096]
    v_4 = [-0.648  -3.2768]
    v_5 = [-0.3888  -2.62144]
    v_6 = [-0.23328  -2.097152]
    v_7 = [-0.139968  -1.6777216]
    v_8 = [-0.0839808  -1.34217728]
    v_9 = [-0.05038848 -1.07374182]
    v_10 = [-0.03023309 -0.85899346]


確かに$(0, 0)$に収束していきますね。これで何が起きているかイメージ付けるために、$f$の勾配の図で勾配矢印を逆方法に向け、その上に$v_i$が通った点を図示してみましょう。


```python
# 上記と同じお絵描き
r = np.linspace(-10, 10, 100)
xx, yy = np.meshgrid(r, r)
zz = 2*xx ** 2 + yy ** 2
fig = plt.figure()
ax = fig.add_subplot()
c = ax.contourf(xx, yy, zz, levels=100)
fig.colorbar(c)

vr = np.linspace(-10, 10, 21)
vx, vy = np.meshgrid(vr, vr)
dfdx = -4 * vx
dfdy = -2 * vy
ax.quiver(vx, vy, dfdx, dfdy, color='white')

ax.plot(vs[:, 0], vs[:, 1], color='red') # 上のセルで計算した最適化の履歴
ax.scatter(vs[:, 0], vs[:, 1], color='red')
```




    <matplotlib.collections.PathCollection at 0x7fe90c3cc250>




![png](gradient-descent_files/gradient-descent_27_1.png)


確かに勾配に従ってそうですね。

一般的に、2次元関数$f(x, y)$が描く曲面は、山と谷のように見えますよね。勾配で最適化をすると、最小値に辿り着くようにいろいろな点を辿るわけですが、その点は必ず前の点より低いところにないといけません。これは言い換えると、山から谷に降りているようなことです。そのイメージから、**Gradient Descent**（勾配降下法）という名前が生まれたのです。

# 勾配降下法と線形回帰

勾配降下法は、関数の最適化を行う方法です。何の関数を最適化するかは全く自由で、その勾配さえ求まれば勾配降下を使うことができます。

今回は、線形回帰に購買降下法を使ってみます。[前回](./linear-regression.html)の内容を思い出してみると、線形回帰ではコスト関数（誤差関数）を最小にするのが目的です。そして、コスト関数は回帰係数$\beta_{ij}$を変数としています。その式を改めて書いてみると以下になります。

$$
J_k(\mathbf{\beta}) = \frac{1}{2}\sum_i^N{\Big(y_k^{(i)} - \hat y_k^{(i)}\Big)^2} = \frac{1}{2}\sum_i^N{\Big(y_k^{(i)} - \sum_j^M \beta_{kj}x_j^{(i)}\Big)^2}
$$

これは、$k$個目の出力（目的変数）に対するコスト$J_k$が、全てのサンプル（データ点）の目的変数の真の値から推測した値を弾いたものの2乗です。さて、この式の勾配は何になるのでしょうか？式を展開してみましょう。


$$
\begin{aligned}
J_k(\mathbf{\beta}) &= \frac{1}{2}\sum_i^N{\Big(y_k^{(i)} - \sum_j^M \beta_{kj}x_j^{(i)}\Big)^2} \\
&= \frac{1}{2}\sum_i^N{ \Big[ (y_k^{(i)})^2 + \Big(\sum_j^M \beta_{kj}x_j^{(i)} \Big)^2 - 2y_k^{(i)}\sum_j^M\Big(\beta_{kj}x_j^{(i)}\Big) \Big]}
\end{aligned}
$$

さて、ここで勾配をとるとどうなるでしょうか？勾配は$\mathbf{\beta}_k$（ベクトル）の要素の個数分の要素を持つわけですので、その一つの要素、$\beta_{kp}$に注目してみましょう。

$$
\def\pd#1{\frac{\partial}{\partial #1}}
\begin{aligned}
(\nabla J_k)_p &= \pd{\beta_{kp}}\frac{1}{2}\sum_i^N{ \Big[ (y_k^{(i)})^2 + \Big(\sum_j^M \beta_{kj}x_j^{(i)} \Big)^2 - 2y_k^{(i)}\sum_j^M\Big(\beta_{kj}x_j^{(i)}\Big) \Big]} \\
&= \frac{1}{2}\sum_i^N{ \Big[ \pd{\beta_{kp}}(y_k^{(i)})^2 + \pd{\beta_{kp}}\Big(\sum_j^M \beta_{kj}x_j^{(i)} \Big)^2 - \pd{\beta_{kp}}2y_k^{(i)}\sum_j^M\Big(\beta_{kj}x_j^{(i)}\Big) \Big]} \\
&= \frac{1}{2}\sum_i^N{\Big[ 2x_p^{(i)}\sum_j^M\Big(\beta_{kj}x_j^{(i)}\Big) - 2y_k^{(i)}x_p^{(i)}\Big]} \\
&= \frac{1}{2}\sum_i^N{2x_p^{(i)}\Big[y_k^{(i)} - \sum_j^M\Big(\beta_{kj}x_j^{(i)}\Big) \Big]} \\
&= \sum_i^N{x_p^{(i)}(y_k^{(i)} - \hat y_k^{(i)})}
\end{aligned}
$$

かなり綺麗な式になってみましたね！これで$\nabla J_k$の全ての要素が同じように求まります。そして、勾配を求めることができたので、後は勾配降下を適用するだけです！そのために、コスト関数とコスト関数の勾配を計算してくれるpython関数と、勾配降下を行い、最適化した答えを返してくれるpython関数を実装しましょう。


```python
# コスト関数は勾配降下では使われませんが、あとから使うので今実装しておきます
def J(B, X, Y):
    yhat = X @ B
    return np.sum((Y - yhat) ** 2, axis=0)

def gradJ(B, X, Y):
    yhat = X @ B
    return np.sum(X * (yhat - Y), axis=0, keepdims=True).T
    
def gradientDescent(X, Y, alpha, iterations):
    B = np.random.rand(X.shape[-1], Y.shape[-1]) # Bの初期値をランダムにする
    Bs = [B] # 通過したBの値を保存
    for i in range(iterations):
        B = B - alpha * gradJ(B, X, Y) # 勾配降下。gJは勾配を計算してくれる関数です
        Bs.append(B)
    return B, Bs
```

これで勾配降下を行う準備ができました。では、実際にデータを読み込んで、実行してみましょう。


```python
X = []
Y = []
# csvファイルからデータを読み込む
with open('data.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        X.append(float(row[0]))
        Y.append(float(row[1]))
X = np.array(X) # pythonのリストをnumpy arrayに変換する
N = X.shape[0]
X = X.reshape(N, 1) # numpyでは、N次元ベクトルとNx1行列は違う扱いになるので、変換しておきます
X = np.append(X, np.ones((N, 1)), axis=1) # データにバイアス用の1の列を追加します
Y = np.array(Y).reshape((N, 1)) # ベクトル -> 行列変換

B, Bs = gradientDescent(X, Y, 0.000013, 100000)
print(B)
```

    [[1368.83257888]
     [8041.73161539]]


勾配降下の結果は$\mathbf{\beta} = (1369, 8042)$となりました。正規方程式で得た値と同じですね！

次に、実際の勾配降下の軌道を描いてみますが、更にコスト関数のあらゆる値を計算してみて、2次平面で色を使って曲面と勾配を表しましょう。


```python
# グラフの範囲
xlim = (-1000, 3000)
ylim = (-1000, 10000)

# 曲面の計算
bx = np.linspace(xlim[0], xlim[1], 100)
by = np.linspace(ylim[0], ylim[1], 100)
bxx, byy = np.meshgrid(bx, by)
bb = np.stack([bxx, byy], axis=2)
B = []
for i in range(100):
    B.append([])
    for j in range(100):
        B[i].append(J(bb[i, j][:, np.newaxis], X, Y))
B = np.array(B).reshape(100, 100)
plt.contourf(bxx, byy, B, levels=100)
plt.colorbar()

# 勾配の計算
V = 20
gx = np.linspace(xlim[0], xlim[1], V)
gy = np.linspace(ylim[0], ylim[1], V)
gxx, gyy = np.meshgrid(gx, gy)
gb = np.stack([gxx, gyy], axis=2)
gB = []
for i in range(V):
    gB.append([])
    for j in range(V):
        gB[i].append(gradJ(gb[i, j][:, np.newaxis], X, Y))
gB = -np.array(gB)
gvx = gB[:, :, 0, 0]
gvy = gB[:, :, 1, 0]
norm = np.sqrt(gvx ** 2 + gvy ** 2)
plt.quiver(gxx, gyy, gvx, gvy, color='white')

# 勾配降下の経路
Bs = np.array(Bs)
plt.scatter(Bs[:, 0, 0], Bs[:, 1, 0], color='red')
```




    <matplotlib.collections.PathCollection at 0x7fe907991a50>




![png](gradient-descent_files/gradient-descent_35_1.png)


少しわかりにくいですが、勾配降下は徐々に$(1369, 8042)$へ近づいていっていますね。最後に、回帰線を描きながら、勾配降下がどのように動いているかを描いてみましょう。


```python
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
ax[0].contourf(bxx, byy, B, levels=100)
ax[1].scatter(X[:, 0], Y)
ax[1].set_xlim(-10, 80)
ax[1].set_ylim(10000, 100000)

dots = ax[0].scatter([], [], color='red')
gd_dots = []
line = ax[1].plot([], [], color='red')[0]

def update(i):
    b = Bs[(2 ** i), :, 0]
    gd_dots.append(b)
    dots.set_offsets(gd_dots)
    xx = np.linspace(-10, 80)
    xx = np.stack([xx, np.ones_like(xx)], axis=1)
    yy = xx @ b
    line.set_data(xx[:, 0], yy)
    
anim = FuncAnimation(fig, update, frames=int(np.log(Bs.shape[0]) / np.log(2)), interval=1000)
plt.close()
HTML(anim.to_html5_video())
```




<video width="864" height="432" controls autoplay loop>
  <source type="video/mp4" src="data:video/mp4;base64,AAAAHGZ0eXBNNFYgAAACAGlzb21pc28yYXZjMQAAAAhmcmVlAADKpG1kYXQAAAKuBgX//6rcRem9
5tlIt5Ys2CDZI+7veDI2NCAtIGNvcmUgMTUyIHIyODU0IGU5YTU5MDMgLSBILjI2NC9NUEVHLTQg
QVZDIGNvZGVjIC0gQ29weWxlZnQgMjAwMy0yMDE3IC0gaHR0cDovL3d3dy52aWRlb2xhbi5vcmcv
eDI2NC5odG1sIC0gb3B0aW9uczogY2FiYWM9MSByZWY9MyBkZWJsb2NrPTE6MDowIGFuYWx5c2U9
MHgzOjB4MTEzIG1lPWhleCBzdWJtZT03IHBzeT0xIHBzeV9yZD0xLjAwOjAuMDAgbWl4ZWRfcmVm
PTEgbWVfcmFuZ2U9MTYgY2hyb21hX21lPTEgdHJlbGxpcz0xIDh4OGRjdD0xIGNxbT0wIGRlYWR6
b25lPTIxLDExIGZhc3RfcHNraXA9MSBjaHJvbWFfcXBfb2Zmc2V0PS0yIHRocmVhZHM9MTIgbG9v
a2FoZWFkX3RocmVhZHM9MiBzbGljZWRfdGhyZWFkcz0wIG5yPTAgZGVjaW1hdGU9MSBpbnRlcmxh
Y2VkPTAgYmx1cmF5X2NvbXBhdD0wIGNvbnN0cmFpbmVkX2ludHJhPTAgYmZyYW1lcz0zIGJfcHly
YW1pZD0yIGJfYWRhcHQ9MSBiX2JpYXM9MCBkaXJlY3Q9MSB3ZWlnaHRiPTEgb3Blbl9nb3A9MCB3
ZWlnaHRwPTIga2V5aW50PTI1MCBrZXlpbnRfbWluPTEgc2NlbmVjdXQ9NDAgaW50cmFfcmVmcmVz
aD0wIHJjX2xvb2thaGVhZD00MCByYz1jcmYgbWJ0cmVlPTEgY3JmPTIzLjAgcWNvbXA9MC42MCBx
cG1pbj0wIHFwbWF4PTY5IHFwc3RlcD00IGlwX3JhdGlvPTEuNDAgYXE9MToxLjAwAIAAAGeJZYiE
ABf//vfUt8yy7VNvtguo96KeJl9DdSUBm5bE7TqAAAADAAADAAADAALclJG8vEL3LzCAAAADABPQ
AfBf90a/4gEOCBVlr2wnqqQw03M6yo0HYJUxW3KrWzOwWFM2Wk0jExo+Ns43C0yHiBfEQeZTv0Td
z4ZXCf6tCpLCvT76fyimRYa5ELwWCuRvD30ILncIWbzjnep9M8loR+OUFjo81BLW2Mc8o7ZxjyBD
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
AExhdmY1Ny44My4xMDA=
">
  Your browser does not support the video tag.
</video>

