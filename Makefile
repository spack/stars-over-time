
all: spack_vs_eb.pdf

spack_vs_eb.pdf: spack_vs_eb.py
	./spack_vs_eb.py

clean:
	rm -f *.pdf

purge: clean
	rm -f *.pyc
	rm -rf repos
