Introduction
============

Many scholars have studied the breakdowns of the networks, e.g.
breakdown of the Internet [@cohen2001breakdown], percolation on random
graphs [@callaway2000network] or in general on the scale-free networks
[@zhao2004attack], [@gallos2005stability]. Many real networks display
community structure, e.g. traffic networks, distribution networks and
electrical power grids. Hence, attention has moved towards such
networks. For instance, in [@wu2006cascade] authors concluded that the
network with small modularity is much easier to trigger cascade failures
than that of the larger one. Hasegawa and Nemoto
[@hasegawa2013hierarchical] studied the random failure on the
hierarchical scale-free networks and indicated their fragility against
both random failure and intentional attacks.

The project aims to study the resilience of the following network
models: (i) Barabasi-Albert model [@albert2002statistical], (ii)
Erdos-Renyi graph [@erdHos1960evolution], (iii) hierarchical random
graph (HRG) [@clauset2008hierarchical], (iv) modified HRG (see Sec.
[2.1](#sec:hrg){reference-type="ref" reference="sec:hrg"}). Multiple
simulations are performed to compare the fragility of these models on
the random and intentional attacks.

The rest of the project is organised as follow. In Sec.
[2](#sec:methods){reference-type="ref" reference="sec:methods"} we
describe the HRG model and define the necessary metrics. Next, in Sec.
[3](#sec:results){reference-type="ref" reference="sec:results"} we
present the results of the random breakdowns and the intentional
attacks. The last section (Sec.
[4](#sec:conclusions){reference-type="ref" reference="sec:conclusions"})
concludes with the final remarks.

Methods {#sec:methods}
=======

Hierarchical random graph {#sec:hrg}
-------------------------

The hierarchical random graph model was proposed by Clauset, Moore and
Newman in [@clauset2008hierarchical]. Authors have used this model to
detect and analyse the hierarchical structure of networks in the real
world. They accomplished this by fitting HRG to observed network data
using tools of statistical inference, combining a maximum-likelihood
approach with a Monte Carlo sampling algorithm on the space of all
possible dendrograms.

The HRG with a specified hierarchical structure is generated using a
dendrogram (Fig. [1](#fig:dendrogram_example){reference-type="ref"
reference="fig:dendrogram_example"}) and a set of probabilities $p_r$
(Tab. [1](#tab:probs){reference-type="ref" reference="tab:probs"}). Each
internal node (sub-community) $r$ of the dendrogram is associated with a
probability $p_r$ that a pair of vertices in the left and right subtrees
of that node are connected. The procedure to generate HRG can be defined
as follows:

-   Construct dendrogram and assign each node probability $p_r$.

-   For the lowest level of hierarchy, set the number of nodes in each
    community (we here set $N_r =1000$, in total $N=8000$).

-   With just specified probabilities, connect nodes in each community
    at the lowest level.

-   Move one level higher and connect nodes between communities with a
    specified probability.

-   Repeat until you reach the root of the dendrogram.

#### Average degree {#average-degree .unnumbered}

In order to compare different network models we have to set the same
average degree. In ER model $\left<k\right> = p(N-1)$, while in BA
$\left< k \right> = 2m$. For HRG the average degree from dendrogram in
Fig. [1](#fig:dendrogram_example){reference-type="ref"
reference="fig:dendrogram_example"} can be calculated as follows:
$$\begin{aligned}
    \left<k\right> = \frac{2 (E_0 + E_1 + E_2 + E_3)}{N},\end{aligned}$$
where $N$ is the total number of nodes i.e.
$N = N_G + N_H + N_I + N_J + N_K + N_L + N_M + N_N$ and $E_i$ is the sum
of all edges at level $i$. At each level we have $$\begin{aligned}
    E_3 &= \frac{1}{2} p_G N_G (N_G - 1) + \frac{1}{2} p_H N_H (N_H - 1) + \dots + \frac{1}{2} p_N N_N (N_N -1), \\
    E_2 &=  \frac{1}{2} p_C (N_G + N_H) (N_G + N_H - 1) + \dots + \frac{1}{2} p_F (N_M + N_N) (N_M + N_N - 1) \\ &= \frac{1}{2} p_C N_C (N_C - 1) + \dots + \frac{1}{2} p_F N_F (N_F - 1), \\
    E_1 &= \frac{1}{2} p_A (N_C + N_D) (N_C + N_D - 1) + \frac{1}{2} p_B (N_E + N_F) (N_E + N_F - 1) \\ &= \frac{1}{2} p_A N_A  (N_A - 1) + \frac{1}{2} p_B N_B (N_B - 1), \\
    E_0 &= \frac{1}{2} p_O (N_A + N_B) (N_A + N_B - 1).\end{aligned}$$

![A dendrogram used for generating hierarchical random
graphs.](figures/dendrogram_example.pdf){#fig:dendrogram_example
width="75%"}

::: {#tab:probs}
   **Node**   **Probability**
  ---------- -----------------
      O            0.001
      A            0.002
      B            0.002
      C            0.002
      D            0.003
      E            0.003
      F            0.003
      G            0.006
      H            0.006
      I            0.006
      J            0.006
      K            0.006
      L            0.006
      M            0.006
      N            0.006

  : The set of probabilities $p_r$ used in the simulations.
:::

An example realization of the HRG is depicted in Fig.
[2](#fig:hrg1_plot){reference-type="ref" reference="fig:hrg1_plot"}.
There are eight communities in total.

![Example realisation of the HRG from dendrogram Fig.
[1](#fig:dendrogram_example){reference-type="ref"
reference="fig:dendrogram_example"} and set of probabilities Tab.
[1](#tab:probs){reference-type="ref" reference="tab:probs"}
($N=8000$).](figures/hrg_test_small.pdf){#fig:hrg1_plot width="65%"}

Attacks on networks
-------------------

#### Metrics {#metrics .unnumbered}

Both in the random breakdowns and the intentional attacks after removal
of $p^*$ nodes ore edges, we measure the size of the giant connected
component (GCC) $N^*$ and the size of the network $N$ and its rescaled
version $S(p^*) = N / N^*$.

#### Random breakdowns {#random-breakdowns .unnumbered}

We remove $p^*$ percent randomly selected **edges** from a given network
and measure the size of the giant connected component. In modified HRG,
we cannot remove the edges between communities. The procedure is
repeated 100 times to obtain reliable results.

#### Intentional attacks {#intentional-attacks .unnumbered}

We remove $p^*$ percent **nodes** with the highest degree from a given
network and also measure the size of GCC. In modified HRG, we cannot
remove the nodes with at least one link between communities. The results
are also averaged over 100 realisations.

Results {#sec:results}
=======

We present the results for the random breakdowns and the intentional
attacks for $\left< k \right> = \{2, 6\}$.

Random breakdowns
-----------------

As expected, the best resilience on the random attacks has the BA model.
Regarding other models, for larger degree ($\left<k \right> = 6$) the
HRG in the basic definition displays the large fluctuations (Fig.
[4](#fig:random_k_2_6){reference-type="ref"
reference="fig:random_k_2_6"}a). Indeed, when we select to remove the
edge between community, the size of the GCC could diminish
significantly. Once we incorporate the "stable" links between
communities, the modified HRG almost matches the ER graph.

![Random breakdowns. Relation between the size of the rescaled giant
connected component and the percent of randomly removed edges $p^*$. (a)
All networks have $\left< k \right> \approx 6$. (b) All networks have
$\left< k \right> \approx 2$.](figures/random_attack_small_k_6.png "fig:"){#fig:random_k_2_6
width="45%"} ![Random breakdowns. Relation between the size of the
rescaled giant connected component and the percent of randomly removed
edges $p^*$. (a) All networks have $\left< k \right> \approx 6$. (b) All
networks have
$\left< k \right> \approx 2$.](figures/random_attack_small_k_2.png "fig:"){#fig:random_k_2_6
width="45%"}

Intentional attacks
-------------------

Figures [6](#fig:intentional_k_2_6){reference-type="ref"
reference="fig:intentional_k_2_6"}a and
[6](#fig:intentional_k_2_6){reference-type="ref"
reference="fig:intentional_k_2_6"}b depict the relationship between the
rescaled size of GCC and the percent of the removed nodes with the
highest degrees. Here the BA model performs the works for both average
degrees. Once again, the modification of HRG reduces the fragility of
the network in both cases. However, the impact is more visible for
$\left<k \right> =6$.

![Intentional attacks. Relation between the size of the rescaled giant
connected component and the percent of removed nodes with the highest
degree $p^*$. (a) All networks have $\left< k \right> \approx 6$. (b)
All networks have
$\left< k \right> \approx 2$.](figures/intentional_attacks_small_k_6.png "fig:"){#fig:intentional_k_2_6
width="45%"} ![Intentional attacks. Relation between the size of the
rescaled giant connected component and the percent of removed nodes with
the highest degree $p^*$. (a) All networks have
$\left< k \right> \approx 6$. (b) All networks have
$\left< k \right> \approx 2$.](figures/intentional_attacks_small_k_2.png "fig:"){#fig:intentional_k_2_6
width="45%"}

Conclusions {#sec:conclusions}
===========

In this project, we study the resilience of three network models: BA, ER
and HRG. The fragility of HRG leads us to modification where we cannot
remove edges between communities. The results show the large
improvements of this proposed modification both in the random breakdowns
and the intentional attacks. We argue that the real network like
electrical power grids between cities should be built so that one should
strengthen the lines between cities.
