# This is the PyAudio distribution makefile.

.PHONY: docs clean

SPHINX_BUILD ?= sphinx-build

VERSION := 0.2.6
DOCS_OUTPUT=docs/

what:
	@echo "make targets:"
	@echo
	@echo " tarball    : build source tarball"
	@echo " docs       : generate documentation (requires sphinx and only works after pyaudio has been installed)"
	@echo " clean      : remove build files"
	@echo
	@echo "To build pyaudio, run:"
	@echo
	@echo "   python setup.py install"

clean:
	@rm -rf build dist MANIFEST $(DOCS_OUTPUT) src/*.pyc

######################################################################
# Documentation
######################################################################

docs:
	$(SPHINX_BUILD) -b html . $(DOCS_OUTPUT)

######################################################################
# Source Tarball
######################################################################
tarball: docs $(SRCFILES) MANIFEST.in
	@python setup.py sdist
