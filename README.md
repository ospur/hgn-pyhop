# HGNpyhop

## Introduction

HGNpyhop is a modification of [Pyhop](https://bitbucket.org/dananau/pyhop/). It works with Hierarchical Goal Networks (HGN) instead of Hierarchical Task Networks (HTN). 

Partly funded by ONR, HGNpyhop is an extension that adds Hierarchical Goal Network capabilities to Pyhop.
Authors of the extension: Weihang Yuan and Hector Munoz-Avila
Version: 1.0
HGNpyhop is released under the Apache License 2.0.

In HGNpyhop, goals (instead of tasks) are decomposed. As per Shivashankar, V. (2015). [Hierarchical goal networks: Formalisms and algorithms for planning and acting (Doctoral dissertation).](https://drum.lib.umd.edu/bitstream/handle/1903/16698/Shivashankar_umd_0117E_16202.pdf):

          Let goals be the list of goals to satisfy

          Case 1: if goals is empty, then return plan

          Let g be the first goal of goals; remove g from goals
          Case 2: if g is satisfied in the state then recursively plan generation
                    for goals
          
          Case 3: If action a has g as an effect and a is applicable then apply a,
                    plan CAT a, and continue recursively plan generation for goals
        
          Case 4: If method m has g as last subgoal and m is applicable, then
          recursive plan generation for (m's subgoals) CAT goals
        
The actual algorithm in Vikas's dissertation combines Cases 3 and 4 to choose between
"RELEVANT" methods and operators. In our implementation it tries actions first
and then it tries methods

When creating a domain, the following requirements must be satisfied:

    - The type of every object must be declared. For every type, list all objects of that type:
            <state>.<type> = {..., <object>,...}
            - Here is an example in the satellite domain:
                    state1.instruments = {'instrument0'}
                    
    - HGNpyhop uses an state-variable representation of the form:
            <state>.<variable>={..., <object>:<value>,...}
            - Here is an example in the satellite domain:
                    state1.power_on = {'instrument0': False}
                    
    - The name of a goal must have the same name as an state variable. It has to indicate the expected value for the object:
            (<variable>,<object>,<value>)
             - Here is an example of a goal:
                ('have_image', 'Phenomenon4', 'thermograph0')

Two examples are provided: the logistics domain and the satellite domain.

## License

[Apache License 2.0](https://github.com/ospur/hgn-pyhop/blob/master/LICENSE)

Pyhop, version 1.2.2 -- a simple SHOP-like planner written in Python.
Author: Dana S. Nau, 2013.05.31

Copyright 2013 Dana S. Nau - http://www.cs.umd.edu/~nau

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

