#[derive(Debug)]
#[allow(dead_code)]
pub enum LocalParams {
    None
}

#[derive(Debug)]
#[allow(dead_code)]
pub struct Linear {
    local_params: Option<Vec<LocalParams>>
}

impl Linear {
    #[inline]
    pub const fn new(local_params: Option<Vec<LocalParams>>) -> Self { Self { local_params }}
}