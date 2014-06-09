probabilistic-ranking
=====================
A framework for performing probabilistic ranking on bibliographic data under ambiguity.

To run:

$ python -m src.main

To run a test:

$ python -m test.<test_name>

To run all tests:

$ nosetests test

The format of the training files are:

(ref)<>(author)_(index)<>(coauthor1):(coauthor2):(coauthorI:)*(coauthorN)<>(venue)<>(name)<>(title)<>

where
- ref is the reference id
- author is the author id
- index is an index within the author's references
- coauthorI is the i-th coauthor
- venue is where it was published (radicals only)
- name if the author name used in this reference
- title is the title of the paper (radicals only)

If possible, the references should be blocked in groups with the same initial and last name, which have an empty line dividing.

The test file has the same format, but author and index have to be any character, or even empty.
