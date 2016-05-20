Sort-Seq Tools 
========

*Quantitative modeling of sequence-function relationships using data from massively parallel assays*

Written by William T. Ireland and Justin B. Kinney  
Current version: 0.01.01  

## Overview

Sort-Seq Tools is a software package for analyzing data from a variety massively parallel assays, including Sort-Seq assays, Massively Parallel Reporter assays, and Deep Mutational Scanning assays. Sort-Seq Tools provides a set of command line routines, which are listed in the [documentation][documentation]. Details can be found in the accompanying paper

Citation: Ireland WT, Kinney JB (2016) Sort-Seq Tools: modeling sequence-function relationships from massively parallel assays. bioRxiv doi:???

## Requriements

Sort-Seq Tools is written in Python 2.9.7 and in Cython 0.23.4. It requires that the following Python packages also be installed: biopython, pymc, scikit-learn, statsmodels, mpmath, pandas, weblogo, and matplotlib. Sort-Seq Tools is currently in alpha testing and has been verified to work on Linux and Mac OS X. 

## Installation

To install Sort-Seq Tools, clone this repository, navigate to the folder containing this README file, and execute

```
python setup.py install
```

Alternatively, Sort-Seq Tools can be installed from PyPI by executing

```
pip install sortseq_tools
```

This approach will also install all of Sort-Seq Tools's dependencies. After Sort-Seq Tools is installed, you can test the functionality of all methods by running

```
sortseq_tools run_tests
```

## Documentation

The commands used to perform the analysis in Ireland & Kinney (2016) are described here [link to analysis.rst]. Documentation on each of the Sort-Seq Tools functions is provided [here][documentation].

## Quick start guide

Below are the commands described in the "Overview" section of the Supplemental Information of Ireland and Kinney (2016). These commands provide a quick entry into the capabilities of Sort-Seq Tools. To execute them, first change to the [examples](examples/) directory, which contains the necessary inpupt files [true_model.txt](examples/true_model.txt) and [genome_ecoli.fa](examples/genome_ecoli.fa)). 

#### Simulating data

Simualte a library of binding sites for the CRP transcription factor:
```
sortseq_tools simulate_library -w TAATGTGAGTTAGCTCACTCAT -n 100000 -m 0.24 -o library.txt
```

Simulate a Sort-Seq experiment using a model ([true_model.txt](examples/true_model.txt)) of CRP-DNA affinity:
```
sortseq_tools simulate_sort -m true_model.txt -n 4 -i library.txt -o dataset.txt
```

#### Computing summary statistics

Compute a mutation profile of the simluated library:
```
sortseq_tools profile_mut -i library.txt -o mutprofile.txt
```

Compute the occurance frequency of each base at each position in the library:
```
sortseq_tools profile_freq -i library.txt -o freqprofile.txt
```

Compute an information profile (a.k.a information footprint) from the simulated data:
```
sortseq_tools profile_info --err -i dataset.txt -o infoprofile.txt
```

#### Inferring quantitative models

Infer a matrix model for CRP from the simulated data:
```
sortseq_tools learn_model -lm LS -mt MAT -i dataset.txt -o matrix_model.txt
```

Infer a neighbor model for CRP from the simulated data:
```
sortseq_tools learn_model -lm LS -mt NBR -i dataset.txt -o neighbor_model.txt
```

#### Evaluating models

Evaluate the inferred matrix model on all sites in the dataset:
```
sortseq_tools evaluate_model -m matrix_model.txt -i dataset.txt -o dataset_with_values.txt
```

Scan the *Escherichia coli* genome ([genome_ecoli.fa](examples/genome_ecoli.fa)) using the inferred matrix model:
```
sortseq_tools scan_model -n 100 -m matrix_model.txt -i genome_ecoli.fa -o genome_sites.txt
```

Compute the predictive information of the inferred matrix model and the true model on the simulated data:
```
sortseq_tools predictiveinfo -m matrix_model.txt -ds dataset.txt
sortseq_tools predictiveinfo -m true_model.txt -ds dataset.txt
```

[documentation]: http://jbkinney.github.io/sortseq_tools/

