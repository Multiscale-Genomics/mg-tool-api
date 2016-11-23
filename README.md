# MuGtoolAPI
A first attempt at outlining the main structures related to the tools section of the VRE.

## Introduction
This is a first attempt at outlining the main structures related to the
tools section of the VRE. It implements the specifications detailed in the
current version (23/09/2016) of the Deliverable 6.1 document: "Design of
computational architecture of software modules" (http://bit.ly/MuGD6_1). It
extends the above document with the aim to provide a simple programming
paradigm to develop tools for the MuG VRE.

The main goals that this proposal aims to achieve are:

1. Achieve horizontal interoperability by defining a "Tool" as a specific
functionality with precise inputs and outputs, which must both comply with the
Data Management Plan (DMP). Tools are implemented as a thin wrappers over
existing software, in order to facilitate integrating existing tools in the
VRE.

2. Achieve vertical interoperability by using COMPSs, and allowing
developers to specify the execution enviroment requirements for each tool by
using COMPSs "constraints" decorator. 

3. Provide a unified, simple paradigm to access the diverse data storage
facilities defined in the DMP, by wrapping data in Python objects (see
"Resource" below) that implement a common API that abstracts the details of
data retrieval; this also makes changes in the DMP transparent to the tools.

4. Simplify the construction of workflows, by conceiving tools such that it is
straightforward to combine them in workflows, using COMPSs "task" decorator and
the COMPSs runtime as the workflow scheduler. 

## Objective

This code is intended as a first draft to fuel discussions among all
involved parties (in particular WP4, WP5 and WP6) about the precise details of
the software architecture of the VRE, and as such won't run as valid Python
code out of the box. Please note that the scientific relevance of this is
limited to providing an example of usage of the class structure proposed.

## Implementation overview

1. Resource:
     It is the general container for all data that is exchanged within the
     VRE. Subclasses, such as the examples outlined below, should deal with the
     details of making the resource available from the various data storage
     facilities defined in the DMP. There should be at least one subclass per
     storage class in the DMP. Every Resource instance is defined by its data
     type, which is immutable. In fact, Resources should probably be immutable
     altogether (in the following they are, but aren't forced to be).  
2. Tool:
     It is the top-level wrapper for tools within the VRE; each tool is defined
     by its input and output formats, and by its specific requirements on the
     execution environment. Tools should implement a "run" method, that defines
     operations needed to get from input to output. Decorating the "run" method
     with "@constraints" allows developers to define the execution environment,
     while decorating with "@task" makes the tool workflow-ready.
3. mug_datatypes:
     A repository of all data types available in MuG; it should closely mirror
     the contents of the DMP. 
4. mug_conversion:
     A library containing commodity functions to perform frequently needed
     conversion operations to and from the formats defined in the DMP. Tool
     developers can also implement their own conversion operations when missing
     from this library.
5. Error handling:
     as a first attempt, the Tool catches all pertinent exceptions, while
     others not related to the Tool should not be caught. The Tool also takes
     care of attaching error information to the output resource.

## Examples

The "example_docking_workflow.py" contains a minimal implementation of a few 
simple example tools in order to perform:

a. Ab-initio predict the structure of a protein given its sequence;
b. Ab-initio predict the structure of a DNA oligomer given its sequence;
c. Rigid-body dock two molecules given their 3D structure.

These tools wrap external resources, Python libraries, binary executables or 
REST APIs, to perform their task; in this example these are not implemented,
but may be replaced with existing tools in the future. Finally, an example
simple workflow is outlined to generate a protein-DNA complex given the
sequence of the two partners using the tools defined above.
