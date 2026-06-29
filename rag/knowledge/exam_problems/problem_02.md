# 高考真题 — 数列

**题目**：已知等差数列 $\{a_n\}$ 满足 $a_3 = 7$，$a_5 + a_7 = 26$。

1. 求 $\{a_n\}$ 的通项公式。
2. 设 $b_n = \frac{1}{a_n a_{n+1}}$，求 $\{b_n\}$ 的前 $n$ 项和 $T_n$。

**解答**：

(1) 设公差为 $d$，则 $a_3 = a_1 + 2d = 7$

$a_5 + a_7 = (a_1 + 4d) + (a_1 + 6d) = 2a_1 + 10d = 26$

解方程组得 $a_1 = 3$，$d = 2$

$\therefore a_n = 3 + (n-1) \cdot 2 = 2n + 1$

(2) $b_n = \frac{1}{(2n+1)(2n+3)} = \frac{1}{2}\left(\frac{1}{2n+1} - \frac{1}{2n+3}\right)$

$T_n = \frac{1}{2}\left[\left(\frac{1}{3} - \frac{1}{5}\right) + \left(\frac{1}{5} - \frac{1}{7}\right) + \cdots + \left(\frac{1}{2n+1} - \frac{1}{2n+3}\right)\right]$

$= \frac{1}{2}\left(\frac{1}{3} - \frac{1}{2n+3}\right) = \frac{n}{3(2n+3)}$
