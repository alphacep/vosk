%module phash

%{
    #define SWIG_FILE_WITH_INIT
    #include "phash.h"
%}

%include "numpy.i"

%init %{
    import_array();
%}

%apply (int DIM1, int DIM2, double* IN_ARRAY2) {(int n1, int n2, double *data)}

%include "phash.h"
