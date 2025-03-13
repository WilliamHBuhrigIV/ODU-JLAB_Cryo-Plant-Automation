use std::{collections::TryReserveError, mem::MaybeUninit, ops::{self, RangeBounds}, slice::SliceIndex, vec::Drain};
use core::fmt;
pub mod file_csv;

////////////////////////////////////////////////////////////////////////////////
// Struct Declarations
////////////////////////////////////////////////////////////////////////////////
#[derive(Copy, Clone)]
#[allow(dead_code)]
pub struct PointData{
    value: f64
}
#[derive(Clone)]
#[allow(dead_code)]
pub struct PointVector{
    buf: Vec<PointData>
}
#[derive(Clone)]
#[allow(dead_code)]
pub struct PointCloud{
    buf: Vec<PointVector>
}

////////////////////////////////////////////////////////////////////////////////
// Inherent methods for PointData
////////////////////////////////////////////////////////////////////////////////

#[allow(dead_code)]
impl PointData {
    #[inline]
    #[must_use]
    pub const fn new(value: f64) -> Self { PointData { value } }
    pub fn get(&self) -> f64 { self.value }
}

////////////////////////////////////////////////////////////////////////////////
// Inherent methods for PointVector
////////////////////////////////////////////////////////////////////////////////

#[allow(dead_code)]
impl PointVector {
    #[inline]
    #[must_use]
    pub const fn new() -> Self { PointVector { buf: Vec::new() } }
    #[inline]
    pub fn with_capacity(capacity: usize) -> Self { PointVector { 
        buf: Vec::with_capacity(capacity) 
    }}
    pub fn reserve(&mut self, additional: usize) {
        self.buf.reserve(additional);
    }
    pub fn reserve_exact(&mut self, additional: usize) {
        self.buf.reserve_exact(additional);
    }
    pub fn try_reserve(&mut self, additional: usize) -> Result<(), TryReserveError> {
        self.buf.try_reserve(additional)
    }
    pub fn try_reserve_exact(&mut self, additional: usize) -> Result<(),TryReserveError> {
        self.buf.try_reserve_exact(additional)
    }
    #[inline]
    pub fn shrink_to_fit(&mut self) {
        self.buf.shrink_to_fit();
    }
    pub fn shrink_to(&mut self, min_capacity: usize) {
        self.buf.shrink_to(min_capacity);
    }
    // Didn't Include Allocator
    pub fn into_boxed_slice(self) -> Box<[PointData]> { 
        self.buf.into_boxed_slice()
    }
    pub fn truncate(&mut self, len: usize) {
        self.buf.truncate(len);
    }
    #[inline]
    pub fn as_slice(&self) -> &[PointData] {
        self.buf.as_slice()
    }
    #[inline]
    pub fn as_mut_slice(&mut self) -> &mut [PointData] {
        self.buf.as_mut_slice()
    }
    #[inline]
    pub fn swap_remove(&mut self, index: usize) -> PointData {
        self.buf.swap_remove(index)
    }
    pub fn insert(&mut self, index: usize, element: PointData) {
        self.buf.insert(index, element);
    }
    pub fn remove(&mut self, index: usize) -> PointData {
        self.buf.remove(index)
    }
    pub fn retain<F>(&mut self, f: F) where F: FnMut(&PointData) -> bool, {
        self.buf.retain(f);
    }
    pub fn retain_mut<F>(&mut self, f: F) where F: FnMut(&mut PointData) -> bool, {
        self.buf.retain_mut(f);
    }
    pub fn dedup_by_key<F, K>(&mut self, key: F) where F: FnMut(&mut PointData) -> K, K: PartialEq, {
        self.buf.dedup_by_key(key);
    }
    pub fn dedup_by<F>(&mut self, same_bucket: F) 
    where 
        F: FnMut(&mut PointData, &mut PointData) -> bool, 
    {
        self.buf.dedup_by(same_bucket);
    }
    #[inline]
    pub fn push(&mut self, value: PointData) {
        self.buf.push(value);
    }
    #[inline]
    pub fn pop(&mut self) -> Option<PointData> {
        self.buf.pop()
    }
    pub fn append(&mut self, other: &mut Self) {
        self.buf.append(&mut other.buf);
    }
    pub fn drain<R>(&mut self, range: R) -> Drain<'_, PointData> where R: RangeBounds<usize>, {
        self.buf.drain(range)
    }
    pub fn clear(&mut self) {
        self.buf.clear();
    }
    // Didn't Include Allocator
    /*pub fn split_off(&mut self, at: usize) -> Self where A: Clone, {
        self.buf.split_off(at)
    }*/
    pub fn resize_with<F>(&mut self, new_len: usize, f: F) where F: FnMut() -> PointData, {
        self.buf.resize_with(new_len, f)
    }
    // Didn't Include Allocator
    /*#[inline]
    pub fn leak<'a>(self) -> &'a mut [PointData] where A: 'a, {
        self.buf.leak()
    }*/
    #[inline]
    pub fn spare_capacity_mut(&mut self) -> &mut [MaybeUninit<PointData>] {
        self.buf.spare_capacity_mut()
    }
    // Too Much Effort 
    /*pub fn resize(&mut self, new_len: usize, value: PointData) {
        let len = self.buf.len();
        if new_len > len {
            self.extend_with(new_len-len, value);
        } else {
            self.truncate(new_len);
        }
    }*/
    // Too Much Effort
    /*pub fn extend_from_slice(&mut self, other: &[PointData]) {
        self.spec_extend(other.iter())
    }*/
    // Use of Unstable Library Feature
    /*pub fn extend_from_within<R>(&mut self, src: R) where R: RangeBounds<usize>, {
        let range = slice::range(src,..self.buf.len());
        self.buf.reserve(range.len());
    }*/
    // No public Vec<T>.into_flattened()
    /*pub fn into_flattened(self) -> Vec<PointData> {
        self.buf.into_flatten()
    }*/
    // Splice is Private?
    /*#[inline]
    pub fn splice<R, I>(&mut self, range: R, replace_with: I) -> Splice<'_, I::IntoIter>
        where R: RangeBounds<usize>, I: IntoIterator<Item = PointData>, {
            Splice { drain: self.drain(range), replace_with: replace_with.into_iter() }
    }*/
}
/*#[allow(dead_code)]
impl PointVector {
    #[inline]
    pub fn dedup(&mut self) {
        self.dedup_by(|a,b| a == b)
    }
}*/

////////////////////////////////////////////////////////////////////////////////
// Inherent methods for PointCloud
////////////////////////////////////////////////////////////////////////////////

#[allow(dead_code)]
impl PointCloud {
    #[inline]
    #[must_use]
    pub const fn new() -> Self { PointCloud { buf: Vec::new() } }
    #[inline]
    pub fn with_capacity(capacity: usize) -> Self { PointCloud { 
        buf: Vec::with_capacity(capacity) 
    }}
    pub fn reserve(&mut self, additional: usize) {
        self.buf.reserve(additional);
    }
    pub fn reserve_exact(&mut self, additional: usize) {
        self.buf.reserve_exact(additional);
    }
    pub fn try_reserve(&mut self, additional: usize) -> Result<(), TryReserveError> {
        self.buf.try_reserve(additional)
    }
    pub fn try_reserve_exact(&mut self, additional: usize) -> Result<(),TryReserveError> {
        self.buf.try_reserve_exact(additional)
    }
    #[inline]
    pub fn shrink_to_fit(&mut self) {
        self.buf.shrink_to_fit();
    }
    pub fn shrink_to(&mut self, min_capacity: usize) {
        self.buf.shrink_to(min_capacity);
    }
    // Didn't Include Allocator
    pub fn into_boxed_slice(self) -> Box<[PointVector]> { 
        self.buf.into_boxed_slice()
    }
    pub fn truncate(&mut self, len: usize) {
        self.buf.truncate(len);
    }
    #[inline]
    pub fn as_slice(&self) -> &[PointVector] {
        self.buf.as_slice()
    }
    #[inline]
    pub fn as_mut_slice(&mut self) -> &mut [PointVector] {
        self.buf.as_mut_slice()
    }
    #[inline]
    pub fn swap_remove(&mut self, index: usize) -> PointVector {
        self.buf.swap_remove(index)
    }
    pub fn insert(&mut self, index: usize, element: PointVector) {
        self.buf.insert(index, element);
    }
    pub fn remove(&mut self, index: usize) -> PointVector {
        self.buf.remove(index)
    }
    pub fn retain<F>(&mut self, f: F) where F: FnMut(&PointVector) -> bool, {
        self.buf.retain(f);
    }
    pub fn retain_mut<F>(&mut self, f: F) where F: FnMut(&mut PointVector) -> bool, {
        self.buf.retain_mut(f);
    }
    pub fn dedup_by_key<F, K>(&mut self, key: F) where F: FnMut(&mut PointVector) -> K, K: PartialEq, {
        self.buf.dedup_by_key(key);
    }
    pub fn dedup_by<F>(&mut self, same_bucket: F) 
    where 
        F: FnMut(&mut PointVector, &mut PointVector) -> bool, 
    {
        self.buf.dedup_by(same_bucket);
    }
    #[inline]
    pub fn push(&mut self, value: PointVector) {
        self.buf.push(value);
    }
    #[inline]
    pub fn pop(&mut self) -> Option<PointVector> {
        self.buf.pop()
    }
    pub fn append(&mut self, other: &mut Self) {
        self.buf.append(&mut other.buf);
    }
    pub fn drain<R>(&mut self, range: R) -> Drain<'_, PointVector> where R: RangeBounds<usize>, {
        self.buf.drain(range)
    }
    pub fn clear(&mut self) {
        self.buf.clear();
    }
    pub fn resize_with<F>(&mut self, new_len: usize, f: F) where F: FnMut() -> PointVector, {
        self.buf.resize_with(new_len, f)
    }
    #[inline]
    pub fn spare_capacity_mut(&mut self) -> &mut [MaybeUninit<PointVector>] {
        self.buf.spare_capacity_mut()
    }
}
#[allow(dead_code)]
/*impl PointCloud {
    #[inline]
    pub fn dedup(&mut self) {
        self.dedup_by(|a,b| a == b)
    }
}*/
#[allow(dead_code)]
impl<I: SliceIndex<[PointVector]>> core::ops::Index<I> for PointCloud {
    type Output = I::Output;
    #[inline]
    fn index(&self, index: I) -> &Self::Output {
        core::ops::Index::index(&**self, index)
    }
}
#[allow(dead_code)]
impl<I: SliceIndex<[PointVector]>> core::ops::IndexMut<I> for PointCloud {
    #[inline]
    fn index_mut(&mut self, index: I) -> &mut Self::Output {
        core::ops::IndexMut::index_mut(&mut **self, index)
    }
}

////////////////////////////////////////////////////////////////////////////////
// Common trait implementations for PointData
////////////////////////////////////////////////////////////////////////////////

#[allow(dead_code)]
impl ops::Deref for PointData {
    type Target = f64;
    #[inline]
    fn deref(&self) -> &f64 {
        &self.value
    }
}
impl fmt::Debug for PointData {
    fn fmt(&self, format: &mut fmt::Formatter<'_>) -> fmt::Result {
        format.debug_tuple(" ")
         .field(&self.value)
         .finish()
    }
}

////////////////////////////////////////////////////////////////////////////////
// Common trait implementations for PointVector
////////////////////////////////////////////////////////////////////////////////

#[allow(dead_code)]
impl ops::Deref for PointVector {
    type Target = [PointData];
    #[inline]
    fn deref(&self) -> &[PointData] {
        self.as_slice()
    }
}
#[allow(dead_code)]
impl ops::DerefMut for PointVector {
    #[inline]
    fn deref_mut(&mut self) -> &mut [PointData] {
        self.as_mut_slice()
    }
}
impl fmt::Debug for PointVector {
    fn fmt(&self, format: &mut fmt::Formatter<'_>) -> fmt::Result {
        //fmt::Debug::fmt(&**self, f)
        format.debug_list()
            .entries(self.buf.iter())
            .finish()
    }
}

////////////////////////////////////////////////////////////////////////////////
// Common trait implementations for PointCloud
////////////////////////////////////////////////////////////////////////////////

#[allow(dead_code)]
impl ops::Deref for PointCloud {
    type Target = [PointVector];
    #[inline]
    fn deref(&self) -> &[PointVector] {
        self.as_slice()
    }
}
#[allow(dead_code)]
impl ops::DerefMut for PointCloud {
    #[inline]
    fn deref_mut(&mut self) -> &mut [PointVector] {
        self.as_mut_slice()
    }
}
impl fmt::Debug for PointCloud {
    fn fmt(&self, format: &mut fmt::Formatter<'_>) -> fmt::Result {
        //fmt::Debug::fmt(&**self, f)
        format.debug_list()
            .entries(self.buf.iter())
            .finish()
    }
}