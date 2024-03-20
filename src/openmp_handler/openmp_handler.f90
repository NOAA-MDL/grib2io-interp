subroutine set_openmp_threads(n)
   use omp_lib
   implicit none

   integer, intent(in) :: n

   call omp_set_num_threads(n)

   return
end subroutine set_openmp_threads

integer function get_openmp_threads() result(n)
   use omp_lib
   implicit none

!$OMP PARALLEL
   n = omp_get_num_threads()
!$OMP END PARALLEL

end function get_openmp_threads
