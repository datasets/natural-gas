version="0.1.0"

DATADIR=data
SCRIPTDIR=scripts

all: data

data:
	python $(SCRIPTDIR)/process.py

clean:
	rm -f $(DATADIR)/*

.PHONY: all data clean
