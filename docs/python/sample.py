# これはコメントです

N = int(input()) # input()で帰ってきた文字列をintに直す

primes = [] # 空リスト（配列）。要素ある場合は[1, 2, 3]

# range(x, y)はx <= i < yの数字が入っている配列を返します。
for i in range(2, N):
    # for 変数 in 配列 - 要素を「変数」に代入して、「配列」を走査します。

    isPrime = True
    for p in primes:
        if i % p == 0:
            isPrime = False
            break
    if isPrime:
        primes.append(i) #配列の後ろに要素を追加
        print(i)
