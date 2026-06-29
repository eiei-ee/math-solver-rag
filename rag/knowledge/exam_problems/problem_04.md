# 考研真题 — 定积分

**题目**：计算 $\int_0^1 x\ln(1+x) \, dx$

**解答**：

使用分部积分法。设 $u = \ln(1+x)$，$dv = x \, dx$

则 $du = \frac{1}{1+x} dx$，$v = \frac{x^2}{2}$

$$\int_0^1 x\ln(1+x) \, dx = \left.\frac{x^2}{2}\ln(1+x)\right|_0^1 - \int_0^1 \frac{x^2}{2} \cdot \frac{1}{1+x} \, dx$$

$$= \frac{1}{2}\ln 2 - \frac{1}{2}\int_0^1 \frac{x^2}{1+x} \, dx$$

处理积分：$\frac{x^2}{1+x} = x - 1 + \frac{1}{1+x}$

$$\int_0^1 \frac{x^2}{1+x} dx = \left[\frac{x^2}{2} - x + \ln(1+x)\right]_0^1 = \frac{1}{2} - 1 + \ln 2$$

$$\therefore \int_0^1 x\ln(1+x) dx = \frac{1}{2}\ln 2 - \frac{1}{2}\left(-\frac{1}{2} + \ln 2\right) = \frac{1}{4}$$
