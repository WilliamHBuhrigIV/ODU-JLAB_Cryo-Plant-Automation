use std::fmt;
use super::heat_exchanger::HeatExchanger;

////////////////////////////////////////////////////////////////////////////////
// Unit/Data Enum Declarations
////////////////////////////////////////////////////////////////////////////////

#[allow(dead_code)]
#[derive(Clone, Debug)]
pub enum Data {
    String(String),
    Float(f64)
}

pub enum Time {
    SQL(Data)
}

pub enum Temperature {
    Kelvin(Data)//, // Primary
    // Celsius(f64),
    // Fahrenheit(f64),
    // Rankine(f64) 
}

pub enum Pressure {
    Pascal(Data)//, // Primary
    // Kilopascal(f64)
}

pub enum Massflow {
    // KilogramPerSecond(f64), // Primary
    GramPerSecond(Data)
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

impl fmt::Display for Data {
    fn fmt(&self, format: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Data::Float(v) => write!(format, "{}", *v),
            Data::String(v) => write!(format, "{}", v)
        }
    }
}

impl fmt::Display for Time {
    fn fmt(&self, format: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Time::SQL(Data::Float(v)) => write!(format, "{}", *v),
            Time::SQL(Data::String(v)) => write!(format, "{}", v)
        }
    }
}

impl fmt::Display for Temperature {
    fn fmt(&self, format: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Temperature::Kelvin(Data::Float(v)) => write!(format, "{}", *v),
            Temperature::Kelvin(Data::String(v)) => write!(format, "{}", v)
        }
    }
}

impl fmt::Display for Pressure {
    fn fmt(&self, format: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Pressure::Pascal(Data::Float(v)) => write!(format, "{}", *v),
            Pressure::Pascal(Data::String(v)) => write!(format, "{}", v)
        }
    }
}

impl fmt::Display for Massflow {
    fn fmt(&self, format: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Massflow::GramPerSecond(Data::Float(v)) => write!(format, "{}", *v),
            Massflow::GramPerSecond(Data::String(v)) => write!(format, "{}", v)
        }
    }
}