# Scripts and data to analysis checklists

created: Peter Woollard 16th May 2023

## Purpose:
To enable an efficient review if the MIX-S checklists proposed by GSC
GSC checklists: https://github.com/GenomicsStandardsConsortium/mixs/tree/main/mixs

The review report is being compiled here:
https://docs.google.com/document/d/1uW6QC8QVaez-hNzWuJ-2BGMIFzUfV8Qw5lPjLCyAIHs/edit?usp=sharing

## Introduction
The Genome Standards Consortium (GSC) generates standard checklists mainly 
for sample related data. Every 2-3 years there is a major version. This needs to
be reviewed by INSDC partners. 

For the review it is necessary to compare the proposed(version 6) with the current(version 5)
and also the checklists terms that are in ENA. ENA may not use all of the standard checklists
and also has checklist terms beyond those.

## How the review is being done
The three sources have been programmatically extracted into JSON and then into python dictionaries.

The intersects and differences between all three have been calculated for both exact and harmonised mapping.
The harmonised mapping currently consists of making all terms lower case, stripping out excess space, etc.