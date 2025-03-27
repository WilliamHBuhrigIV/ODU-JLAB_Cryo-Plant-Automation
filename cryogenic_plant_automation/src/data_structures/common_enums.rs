use std::fmt;
use super::heat_exchanger::HeatExchanger;

////////////////////////////////////////////////////////////////////////////////
// Unit Enum Declarations
////////////////////////////////////////////////////////////////////////////////

pub enum Temperature {
    Kelvin(f64)//, // Primary
    // Celsius(f64),
    // Fahrenheit(f64),
    // Rankine(f64) 
}

pub enum Pressure {
    Pascal(f64)//, // Primary
    // Kilopascal(f64)
}

pub enum Massflow {
    // KilogramPerSecond(f64), // Primary
    GramPerSecond(f64)
}

////////////////////////////////////////////////////////////////////////////////
// Materials Enum Declarations
////////////////////////////////////////////////////////////////////////////////

#[allow(dead_code)]
pub enum Fluid {
    Helium,
    Nitrogen
}

#[allow(dead_code)]
pub enum Phase {
    Liquid,
    Gas,
    TwoPhase // Gas-Liquid
}

pub enum Component<'a> {
    HeatExchanger(&'a HeatExchanger)
}

////////////////////////////////////////////////////////////////////////////////
// Debug Declarations
////////////////////////////////////////////////////////////////////////////////

impl fmt::Display for Temperature {
    fn fmt(&self, format: &mut fmt::Formatter<'_>) -> fmt::Result {
        match *self {
            Temperature::Kelvin(v) => write!(format, "{}", v)
        }
    }
}

impl fmt::Display for Pressure {
    fn fmt(&self, format: &mut fmt::Formatter<'_>) -> fmt::Result {
        match *self {
            Pressure::Pascal(v) => write!(format, "{}", v)
        }
    }
}

impl fmt::Display for Massflow {
    fn fmt(&self, format: &mut fmt::Formatter<'_>) -> fmt::Result {
        match *self {
            Massflow::GramPerSecond(v) => write!(format, "{}", v)
        }
    }
}