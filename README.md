# mg-tool-api

[![Documentation Status](https://readthedocs.org/projects/mg-tool-api/badge/?version=latest)](http://mg-tool-api.readthedocs.io/en/latest/?badge=latest)

## Introduction
This library implements the specifications detailed in the
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

## Implementation overview
1. Tool:
	Is the top-level wrapper for tools within the VRE; each tool is defined
	by its input and output formats, and by its specific requirements on the
	execution environment. Tools should implement a "run" method, that defines
	operations needed to get from input to output. The "run" method calls other
	methods which are decorated using PyCOMPSs "@task" and "@constraints",
	allowing tool developers to define the workflow and execution environment.
2. App:
	Is the main entry point to the tools layer of the VRE; it deals with heterogeneity
	in the way Tools are run, in terms of filesystem access, runtime environment,
	error reporting, and more. Therefore, Apps are compatible with all Tools.
	Apps implement a "launch" method, which prepares and runs a single instance of Tool.
	The "apps" module provides some example Apps for straightforward cases:

	- *LocalApp*: uses the MuG DMP API to retrieve file names that are assumed
	to be locally accessible;

	- *PyCOMPSsApp*: specific for Tools using PyCOMPSs;

	- *WorkflowApp*: inherits from both of the above, and implements the ability
	to unstage intermediate outputs.

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

See the documentation for the classes for more information.

## Examples

The "examples" module contains usage examples.

The "summer.py" example implements a workflow using PyCOMPSs.
