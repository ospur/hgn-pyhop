# HGNpyhop

## Introduction

HGNpyhop is a modification of [Pyhop](https://bitbucket.org/dananau/pyhop/). It works with Hierarchical Goal Networks (HGN) instead of Hierarchical Task Networks (HTN).

In HGNpyhop, goals (instead of tasks) are decomposed. As per Shivashankar, V. (2015). [Hierarchical goal networks: Formalisms and algorithms for planning and acting (Doctoral dissertation).](https://drum.lib.umd.edu/bitstream/handle/1903/16698/Shivashankar_umd_0117E_16202.pdf):

Case 1: if tasks is empty, then return plan

Case 2: Let g be the first goal of tasks; remove g from tasks; if g is satisfied in the state then recursively plan generation for tasks
          
Case 3: If action a has g as an effect and a is applicable then apply a, plan CAT a, and continue recursively plan generation for tasks
        
Case 4: If method m has g as last subgoal and m is applicable, then recursive plan generation for (method subgoals) CAT tasks
The actual algorithm in the paper combines Cases 3 and 4 to choose between "RELEVANT" methods and operators.

Two examples are provided: the logistics domain and the satellite domain.

## License

[Apache License 2.0](https://github.com/ospur/hgn-pyhop/blob/master/LICENSE)
