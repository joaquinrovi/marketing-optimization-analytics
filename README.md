# Multi objective - Multi product - Multi media channel optimization tool

## Channel-product model

* **Maximize:**

$$ \sum_{i \in C \cup L \subset I}\sum_{j \in J} \mathbb{E}[R_{i,j}^{imp}]*\mathbb{E}[R_{i,j}^{conv}]*x_{i,j} $$
$$ \sum_{i \in L \cup C \subset I}\sum_{j \in J} \mathbb{E}[R_{i,j}^{imp}]*\mathbb{E}[R_{i,j}^{leads}]*x_{i,j} $$
$$ \sum_{i \in I}\sum_{j \in J} \mathbb{E}[R_{i,j}^{imp}]*\mathbb{E}[R_{i,j}^{clicks}]*x_{i,j} $$

* **Minimize:**

$$ \sum_{i \in C \cup L \subset I}\sum_{j \in J} \mathbb{E}[R_{i,j}^{cpa}]*\frac{x_{i,j}}{\Beta} $$
$$ \sum_{i \in L \cup C \subset I}\sum_{j \in J} \mathbb{E}[R_{i,j}^{cpl}]*\frac{x_{i,j}}{\Beta} $$

**Subject to:**

$ \sum_{i \in I} \sum_{j \in J} x_{i,j} = \Beta $

$ \beta_{j}^{inf} \leq \sum_{i \in I} x_{i,j} \leq \beta_{j}^{sup}, \forall j \in J $

$ \omega_{i}^{min} \leq \sum_{j \in J} \frac{x_{i,j}}{\Beta} \leq \omega_{i}^{max}, \forall i \in I $

$ \sum_{i \in I}\sum_{j \in J} \mathbb{E}[R_{i,j}^{imp}]*\mathbb{E}[R_{i,j}^{clicks}]*x_{i,j} \geq \Gamma $

$ \sum_{i \in C \cup L \subset I}\sum_{j \in J} \mathbb{E}[R_{i,j}^{imp}]*\mathbb{E}[R_{i,j}^{conv}]*x_{i,j} \geq \Mu $

$ \sum_{i \in L \cup C \subset I}\sum_{j \in J} \mathbb{E}[R_{i,j}^{imp}]*\mathbb{E}[R_{i,j}^{leads}]*x_{i,j} \geq \Pi $

$ \sum_{i \in C \cup L \subset I}\sum_{j \in J} \mathbb{E}[R_{i,j}^{cpa}]*\frac{x_{i,j}}{\Beta} \leq \Delta $

$ \sum_{i \in L \cup C \subset I}\sum_{j \in J} \mathbb{E}[R_{i,j}^{cpl}]*\frac{x_{i,j}}{\Beta} \leq \Omicron $

$ \sum_{j \in J}\sum_{k \in J} \frac{x_{i,j}*x_{i,k}*\sigma_{j,k,i}}{\Beta} \leq \sigma_{i}^{2}, \forall i \in I $

$ \sum_{j \in J}\sum_{k \in J} \frac{u_{i,j,k}*\sigma_{j,k,i}}{\Beta} \leq \sigma_{i}^{2}, \forall i \in I $

$ u_{i,j,k} \geq x_{i,j}^{L}x_{i,k} + x_{i,j}x_{i,k}^{L} - x_{i,j}^{L}x_{i,k}^{L}, \forall (j,k) \in J, \forall i \in I  $

$ u_{i,j,k} \geq x_{i,j}^{U}x_{i,k} + x_{i,j}x_{i,k}^{U} - x_{i,j}^{U}x_{i,k}^{U}, \forall (j,k) \in J, \forall i \in I  $

$ u_{i,j,k} \leq x_{i,j}^{U}x_{i,k} + x_{i,j}x_{i,k}^{L} - x_{i,j}^{U}x_{i,k}^{L}, \forall (j,k) \in J, \forall i \in I  $

$ u_{i,j,k} \leq x_{i,j}x_{i,k}^{U} + x_{i,j}^{L}x_{i,k} - x_{i,j}^{L}x_{i,k}^{U}, \forall (j,k) \in J, \forall i \in I  $

$ x_{i,j} \geq 0, \forall i \in I, \forall j \in J $

$ u_{i,j,k} \geq 0, \forall (j,k) \in J, \forall i \in I $

## Product model

* **Maximize:**

$$ \sum_{i \in I} \mathbb{E}[R_{i}^{conv}] * y_{i} $$

$$ \sum_{i \in I} \mathbb{E}[R_{i}^{leads}] * y_{i} $$

* **Minimize:**

$$ \sum_{i \in I}\sum_{p \in I} y_{i}*y_{p}*\Sigma_{i,p}^{total} $$
$$ \sum_{i \in I}\sum_{p \in I} z_{i,p}*\Sigma_{i,p}^{total} $$
$$ \sum_{i \in I} \mathbb{E}[R_{i}^{cpa}] * y_{i} $$
$$ \sum_{i \in I} \mathbb{E}[R_{i}^{cpl}] * y_{i} $$

**Subject to:**

$ \sum_{i \in I} y_{i} = 1 $

$ \omega_{i}^{min} \leq y_{i} \leq \omega_{i}^{max}, \forall i \in I $

$ \sum_{i \in I} \mathbb{E}[R_{i}^{conv}] * y_{i} \geq \Nu_1 $

$ \sum_{i \in I} \mathbb{E}[R_{i}^{leads}] * y_{i} \geq \Nu_2 $

$ \sum_{i \in I} \mathbb{E}[R_{i}^{cpa}] * y_{i} \leq C_1 $

$ \sum_{i \in I} \mathbb{E}[R_{i}^{cpl}] * y_{i} \leq C_2 $

$ \sum_{i \in I}\sum_{p \in I} y_{i}*y_{p}*\Sigma_{i,p}^{total} \leq \sigma_{total}^{2} $

$ \sum_{i \in I}\sum_{p \in I} z_{i,p}*\Sigma_{i,p}^{total} \leq \sigma_{total}^{2} $

$ z_{i,p} \geq y_{i}^{L}y_{p} + y_{i}y_{p}^{L} - y_{i}^{L}y_{p}^{L}, \forall(i,p) \in I $

$ z_{i,p} \geq y_{i}^{U}y_{p} + y_{i}y_{p}^{U} - y_{i}^{U}y_{p}^{U}, \forall(i,p) \in I $

$ z_{i,p} \leq y_{i}^{U}y_{p} + y_{i}y_{p}^{L} - y_{i}^{U}y_{p}^{L}, \forall(i,p) \in I $

$ z_{i,p} \leq y_{i}y_{p}^{U} + y_{i}^{L}y_{p} - y_{i}^{L}y_{p}^{U}, \forall(i,p) \in I $

$ 0 \leq y_{i} \leq 1, \forall i \in I $

$ z_{i,p} \geq 0, \forall(i,p) \in I $
