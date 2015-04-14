module sll_box_splines
#include "sll_working_precision.h"
#include "sll_memory.h"
#include "sll_assert.h"
#include "sll_splines.h"
#include "sll_utilities.h"
#include "sll_boundary_condition_descriptors.h"
use hex_pre_filters
use sll_hex_meshes
use fekete_integration

implicit none

type sll_box_spline_2d
   type(sll_hex_mesh_2d), pointer  :: mesh !< Hexagonal mesh
   sll_int32 SLL_PRIV :: bc_type !< Boundary conditions definition
   sll_real64, dimension(:), pointer :: coeffs !< Spline coefficients
end type sll_box_spline_2d



contains  ! ****************************************************************


#define MAKE_GET_SLOT_FUNCTION( fname, datatype, slot, ret_type )    \
  function fname( spline_obj ) result(val);                \
    type(datatype), pointer :: spline_obj;                 \
    ret_type :: val;                                       \
    val = spline_obj%slot;                                 \
  end function fname


  function new_box_spline_2d( &
       mesh,         &
       bc_type)

    type(sll_box_spline_2d), pointer  :: new_box_spline_2d
    type(sll_hex_mesh_2d),   pointer  :: mesh
    sll_int32,  intent(in)        :: bc_type
    sll_int32                     :: ierr


    SLL_ALLOCATE( new_box_spline_2d, ierr )

    new_box_spline_2d%mesh => mesh

    new_box_spline_2d%bc_type = bc_type

    SLL_ALLOCATE( new_box_spline_2d%coeffs(1:mesh%num_pts_tot), ierr )

  end function new_box_spline_2d

end module sll_box_splines
