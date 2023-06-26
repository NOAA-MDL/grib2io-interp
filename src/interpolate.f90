subroutine interpolate_scalar(ip,ipopt,igdtnumi,igdtmpli,igdtleni,igdtnumo,igdtmplo,&
                              igdtleno,mi,mo,km,ibi,li,gi,no,ibo,lo,go,rlat,rlon,iret)
use ipolates_mod
implicit none

! ---------------------------------------------------------------------------------------- 
! Input/Output Variables
! ---------------------------------------------------------------------------------------- 
integer, intent(in) :: ip
integer, intent(in), dimension(20) :: ipopt
integer, intent(in) :: igdtnumi
integer, intent(in), dimension(igdtleni) :: igdtmpli
integer, intent(in) :: igdtleni
integer, intent(in) :: igdtnumo
integer, intent(in), dimension(igdtleno) :: igdtmplo
integer, intent(in) :: igdtleno
integer, intent(in) :: mi
integer, intent(in) :: mo
integer, intent(in) :: km
integer, intent(in), dimension(km) :: ibi
logical(kind=1), intent(in), dimension(mi,km) :: li
real, intent(in), dimension(mi,km) :: gi
integer, intent(out) :: no 
integer, intent(out), dimension(km) :: ibo
logical(kind=1), intent(out), dimension(mo,km) :: lo
real, intent(out), dimension(mo,km) :: go
real, intent(inout), dimension(mo) :: rlat
real, intent(inout), dimension(mo) :: rlon
integer, intent(out) :: iret 

! ---------------------------------------------------------------------------------------- 
! Initialize
! ---------------------------------------------------------------------------------------- 
iret=0
no=0

! ---------------------------------------------------------------------------------------- 
! Call NCEPLIBS-ip subroutine, ipolates_grib2 to perform interpolation of scalar fields
! using GRIB2 metadata.
! ---------------------------------------------------------------------------------------- 
call ipolates_grib2(ip,ipopt,igdtnumi,igdtmpli,igdtleni,igdtnumo,igdtmplo,igdtleno, &
                    mi,mo,km,ibi,li,gi,no,rlat,rlon,ibo,lo,go,iret)

return
end subroutine interpolate_scalar
! ---------------------------------------------------------------------------------------- 
! ---------------------------------------------------------------------------------------- 
! ---------------------------------------------------------------------------------------- 
subroutine interpolate_vector(ip,ipopt,igdtnumi,igdtmpli,igdtleni,igdtnumo,igdtmplo,&
                              igdtleno,mi,mo,km,ibi,li,ui,vi,no,ibo,lo,uo,vo,rlat,rlon,&
                              crot,srot,iret)
use ipolatev_mod
implicit none

! ---------------------------------------------------------------------------------------- 
! Input/Output Variables
! ---------------------------------------------------------------------------------------- 
integer, intent(in) :: ip
integer, intent(in), dimension(20) :: ipopt
integer, intent(in) :: igdtnumi
integer, intent(in), dimension(igdtleni) :: igdtmpli
integer, intent(in) :: igdtleni
integer, intent(in) :: igdtnumo
integer, intent(in), dimension(igdtleno) :: igdtmplo
integer, intent(in) :: igdtleno
integer, intent(in) :: mi
integer, intent(in) :: mo
integer, intent(in) :: km
integer, intent(in), dimension(km) :: ibi
logical(kind=1), intent(in), dimension(mi,km) :: li
real, intent(in), dimension(mi,km) :: ui
real, intent(in), dimension(mi,km) :: vi
integer, intent(out) :: no
integer, intent(out), dimension(km) :: ibo
logical(kind=1), intent(out), dimension(mo,km) :: lo
real, intent(out), dimension(mo,km) :: uo
real, intent(out), dimension(mo,km) :: vo
real, intent(inout), dimension(mo) :: rlat
real, intent(inout), dimension(mo) :: rlon
real, intent(inout), dimension(mo) :: crot
real, intent(inout), dimension(mo) :: srot
integer, intent(out) :: iret

! ---------------------------------------------------------------------------------------- 
! Initialize
! ---------------------------------------------------------------------------------------- 
iret=0
no=0

! ---------------------------------------------------------------------------------------- 
! Call NCEPLIBS-ip subroutine, ipolatev_grib2 to perform interpolation of vector fields
! using GRIB2 metadata.
! ---------------------------------------------------------------------------------------- 
call ipolatev_grib2(ip,ipopt,igdtnumi,igdtmpli,igdtleni,igdtnumo,igdtmplo,igdtleno,&
                    mi,mo,km,ibi,li,ui,vi,no,rlat,rlon,crot,srot,ibo,lo,uo,vo,iret)

return
end subroutine interpolate_vector
