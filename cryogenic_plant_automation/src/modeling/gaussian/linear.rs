#[derive(Debug)]
pub enum LocalParams {
    None
}

#[derive(Debug)]
pub struct Linear {
    #[allow(dead_code)]
    local_params: Option<Vec<LocalParams>>
}

impl Linear {
    #[inline]
    pub const fn new(local_params: Option<Vec<LocalParams>>) -> Self { Self { local_params }}
    #[inline]
    pub fn compute(&self) { println!("Got to Linear!") }
}