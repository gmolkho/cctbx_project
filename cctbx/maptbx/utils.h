#ifndef CCTBX_MAPTBX_UTILS_H
#define CCTBX_MAPTBX_UTILS_H

#include <cstddef>
#include <scitbx/array_family/accessors/c_grid.h>
#include <scitbx/array_family/accessors/flex_grid.h>
#include <cctbx/uctbx.h>


namespace cctbx { namespace maptbx {

  //! Miller index element corresponding to 1-dimensional array index.
  template <typename IntegerType>
  inline
  IntegerType
  ih_as_h(IntegerType ih, std::size_t n_real)
  {
    if (ih <= n_real/2) return ih;
    return ih - n_real;
  }

  //! 1-dimensional array index corresponding to Miller index element.
  /*! Returns -1 if h is out of range (see code).
   */
  template <typename IntegerType>
  inline
  IntegerType
  h_as_ih_exact(IntegerType h, IntegerType n_complex, bool positive_only)
  {
    if (positive_only) {
      if (0 > h || h >= n_complex) return -1;
    }
    else {
      IntegerType m = (n_complex - 1) / 2;
      if (-m > h || h > m) return -1;
      else if (h < 0) return h + n_complex;
    }
    return h;
  }

  //! 3-dimensional array indices corresponding to Miller index.
  /*! Result is -1 for out-of-range elements (see code).
   */
  template <typename IndexTypeN>
  af::int3
  h_as_ih_exact_array(bool anomalous_flag,
                      miller::index<> const& h,
                      IndexTypeN const& n_complex)
  {
    af::int3 ih;
    bool positive_only[] = {false, false, !anomalous_flag};
    for(std::size_t i=0;i<3;i++) {
      ih[i] = h_as_ih_exact(h[i], n_complex[i], positive_only[i]);
    }
    return ih;
  }

  //! 1-dimensional array index corresponding to Miller index element.
  /*! Applies modulus operation (see code).
   */
  template <typename IntegerType>
  inline
  IntegerType
  h_as_ih_mod(IntegerType h, IntegerType const& n_real)
  {
    h %= n_real;
    if (h < 0) h += n_real;
    return h;
  }

  //! 3-dimensional array indices corresponding to Miller index.
  /*! Applies modulus operation (see code).
      <p>
      See also: structure_factors::to_map
   */
  template <typename IndexTypeN>
  inline
  IndexTypeN
  h_as_ih_mod_array(miller::index<> const& h, IndexTypeN const& n_real)
  {
    IndexTypeN ih;
    for(std::size_t i=0;i<3;i++) {
      ih[i] = h_as_ih_mod(h[i], n_real[i]);
    }
    return ih;
  }

template <typename DataType>
void hoppe_gassman_modification2(af::ref<DataType, af::c_grid<3> > map_data,
       DataType mean_scale, int n_iterations)
/* A modified version of rho->3*rho^2-2*rho^3 modification.
   Acta Cryst. (1968). B24, 97-107
   Acta Cryst. (1975). A31, 388-389
   Acta Cryst. (1979). B35, 1776-1785
*/
{
  int nx = map_data.accessor()[0];
  int ny = map_data.accessor()[1];
  int nz = map_data.accessor()[2];
  for(int iter = 0; iter < n_iterations; iter++) {
    for(int i = 0; i < nx; i++) {
      for(int j = 0; j < ny; j++) {
        for(int k = 0; k < nz; k++) {
           DataType rho = map_data(i,j,k);
           if(rho<0) map_data(i,j,k) = 0;
           if(rho >=0 && rho<=1) {
             DataType rho_sq = rho*rho;
             map_data(i,j,k) = 3*rho_sq - 2*rho*rho_sq;
    }}}}
  }
}


template <typename DataType>
void hoppe_gassman_modification(af::ref<DataType, af::c_grid<3> > map_data,
       DataType mean_scale, int n_iterations)
/* A modified version of rho->3*rho^2-2*rho^3 modification.
   Acta Cryst. (1968). B24, 97-107
   Acta Cryst. (1975). A31, 388-389
   Acta Cryst. (1979). B35, 1776-1785
*/
{
  int nx = map_data.accessor()[0];
  int ny = map_data.accessor()[1];
  int nz = map_data.accessor()[2];
  for(int iter = 0; iter < n_iterations; iter++) {
    DataType rho_mean = 0;
    DataType rho_max = 0;
    int cntr = 0;
    for(int i = 0; i < nx; i++) {
      for(int j = 0; j < ny; j++) {
        for(int k = 0; k < nz; k++) {
          DataType rho = map_data(i,j,k);
          if(rho>0) {
            rho_mean += rho;
            cntr += 1;
            if(rho>rho_max) rho_max = rho;
    }}}}
    if(cntr != 0) rho_mean /= cntr;
    DataType rho_ms = rho_mean*mean_scale;
    if(rho_max!=0) {
      for(int i = 0; i < nx; i++) {
        for(int j = 0; j < ny; j++) {
          for(int k = 0; k < nz; k++) {
             DataType rho = map_data(i,j,k);
             if(rho > rho_ms) rho = rho_ms;
             CCTBX_ASSERT(rho<=rho_max);
             rho /= rho_max;
             if(rho<0) map_data(i,j,k) = 0;
             else {
               DataType rho_sq = rho*rho;
               map_data(i,j,k) = 3*rho_sq - 2*rho*rho_sq;
    }}}}}
  }
}

template <typename DataType>
void set_box(
  af::const_ref<DataType, af::c_grid<3> > const& map_data_from,
  af::ref<DataType, af::c_grid<3> > map_data_to,
  af::tiny<int, 3> const& start,
  af::tiny<int, 3> const& end)
{
  int ii=0;
  for (int i = start[0]; i < end[0]; i++) {
    int jj=0;
    for (int j = start[1]; j < end[1]; j++) {
      int kk=0;
      for (int k = start[2]; k < end[2]; k++) {
        map_data_to(i,j,k) = map_data_from(ii,jj,kk);
        kk+=1;
      }
      jj+=1;
    }
    ii+=1;
  }
}

template <typename DataType>
void cut_by(
       af::ref<DataType, af::c_grid<3> > kick,
       af::ref<DataType, af::c_grid<3> > fem)
{
  af::tiny<int, 3> a1 = kick.accessor();
  af::tiny<int, 3> a2 = fem.accessor();
  for(int i = 0; i < 3; i++) CCTBX_ASSERT(a1[i]==a2[i]);
  for(int i = 0; i < a1[0]; i++) {
    for(int j = 0; j < a1[1]; j++) {
      for(int k = 0; k < a1[2]; k++) {
         if(kick(i,j,k)<0.5) {
           kick(i,j,k)=0;
  }}}}
  for(int i = 0; i < a1[0]; i++) {
    for(int j = 0; j < a1[1]; j++) {
      for(int k = 0; k < a1[2]; k++) {
         if(fem(i,j,k)<1) {
           fem(i,j,k)=0;
  }}}}

  for(int i = 0; i < a1[0]; i++) {
    for(int j = 0; j < a1[1]; j++) {
      for(int k = 0; k < a1[2]; k++) {
         double rk = kick(i,j,k);
         double rf = fem(i,j,k);
         if(rk==0 || rf==0) {
           kick(i,j,k)=0;
           fem(i,j,k)=0;
  }}}}
}


template <typename DataType>
void intersection(
       af::ref<DataType, af::c_grid<3> > map_data_1,
       af::ref<DataType, af::c_grid<3> > map_data_2,
       DataType threshold)
{
  af::tiny<int, 3> a1 = map_data_1.accessor();
  af::tiny<int, 3> a2 = map_data_2.accessor();
  for(int i = 0; i < 3; i++) CCTBX_ASSERT(a1[i]==a2[i]);
  for(int i = 0; i < a1[0]; i++) {
    for(int j = 0; j < a1[1]; j++) {
      for(int k = 0; k < a1[2]; k++) {
         double rho1 = map_data_1(i,j,k);
         double rho2 = map_data_2(i,j,k);
         bool c1 = rho1>threshold && rho2<threshold;
         bool c2 = rho2>threshold && rho1<threshold;
         if(c1 || c2) {
           map_data_1(i,j,k)=0;
           map_data_2(i,j,k)=0;
  }}}}
}

template <typename DataType>
void convert_to_non_negative(
       af::ref<DataType, af::c_grid<3> > map_data,
       DataType substitute_value)
{
  int nx = map_data.accessor()[0];
  int ny = map_data.accessor()[1];
  int nz = map_data.accessor()[2];
  double rho_max = af::max(map_data);
  for(int i = 0; i < nx; i++) {
    for(int j = 0; j < ny; j++) {
      for(int k = 0; k < nz; k++) {
         double rho = map_data(i,j,k);
         if(rho<0) map_data(i,j,k) = substitute_value;
  }}}
}

template <typename DataType>
void reset(
       af::ref<DataType, af::c_grid<3> > map_data,
       DataType substitute_value,
       DataType less_than_threshold)
{
  int nx = map_data.accessor()[0];
  int ny = map_data.accessor()[1];
  int nz = map_data.accessor()[2];
  double rho_max = af::max(map_data);
  for(int i = 0; i < nx; i++) {
    for(int j = 0; j < ny; j++) {
      for(int k = 0; k < nz; k++) {
         double rho = map_data(i,j,k);
         if(rho<less_than_threshold) map_data(i,j,k) = substitute_value;
  }}}
}

}} // namespace cctbx::maptbx

#endif // CCTBX_MAPTBX_UTILS_H
