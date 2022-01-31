library(pryr)



for (n in 9:11) {



    k = 2^n



    cat(k, system.time(matrix(runif(k*k), nrow=k))[3], '\n')



    cat('tiempo', k, system.time(matrix(runif(k*k), nrow=k))[3], '\n')



    cat('memoria', k, object_size(matrix(runif(k*k), nrow=k)), '\n')



}
