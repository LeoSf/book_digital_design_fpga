# Repository: Digital Design of Signal Processing Systems - Personal Exercises

Leandro D. Medus  
[ August 2020 ]

Leandro D. Medus

The current repository contains examples and personal notes about the book:

Digital Design of Signal Processing Systems
A Practical Approach
Shoab Ahmed Khan
Wiley (2011)


---
**Summary**  
TBD

## Table of Content
TBD

## Ch2. Using a Hardware Description Language
* Exercise 2.1:


## Notes:

``tcl
D:\Repos\FPGA\book_circuit_design_2010\scripts>

vivado -mode batch -source auto_generate_project.tcl -tclargs --origin_dir ../ch5 --project_name ex_5.1  --module_name mux
``

``sh
D:\Repos\FPGA\book_circuit_design_2010\scripts>

python generate_test_bench.py ..\ch4\poc_alias\src\poc_alias.vhd

 python generate_test_bench.py ../ch7/ex_7.6/src/dual_edge.vhd
``
