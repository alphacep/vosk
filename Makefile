CC=gcc
NUMPYFLAGS=-I /usr/local/lib/python3.6/dist-packages/numpy/core/include
CFLAGS=-g -O2 `pkg-config python3 --cflags` ${NUMPYFLAGS}
LIBS=`pkg-config python3 --libs`

all: _phash.so

_phash.so: phash.c phash.h phash_wrap.c
	$(CXX) $(CFLAGS) -fPIC -shared -o $@ phash.c phash_wrap.c

phash_wrap.c: phash.i
	swig -python -o phash_wrap.c phash.i

clean:
	$(RM) *.so phash_wrap.c *.o *.pyc
