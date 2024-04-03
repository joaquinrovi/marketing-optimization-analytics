# -*- coding: utf-8 -*-
"""
objetives_prod.py
====================================
Functions for the objectives of the mathematical model (product planning).

@author:
     - j.rodriguez.villegas
"""

from pyomo.environ import *

def create_objective(model):
    model.obj_funct_aggregated_2 = Objective(sense = maximize, rule = aggregated_objective_2)

# Multi-objetive functions
weight_total_leads = 0 
weight_total_conversions = 0 
weight_total_cpa = 0
weight_total_cpl = 0
weight_total_risk = -1

def aggregated_objective_2(model):
    '''
    This function creates the aggregated multi objective functions.

    Parameters
    ----------
    model : Pyomo ConcreteModel
        The optimization model.

    Return
    ------------
    double
        Total expected multi-objective function.
    '''
    return (
        weight_total_leads * calculate_total_leads(model) + 
        weight_total_conversions * calculate_total_conversions(model) +
        weight_total_cpa * calculate_total_CPA(model) + 
        weight_total_cpl * calculate_total_CPL(model) + 
        weight_total_risk * calculate_total_risk_prod(model)
    )

def calculate_total_conversions(model):
    '''
    This function calculates the total expected conversions.

    Parameters
    ----------
    model : Pyomo ConcreteModel
        The optimization model.

    Return
    ------------
    double
        Total expected conversions.
    '''
    total_conversions = sum(model.expected_conversions[i] * model.y[i] for i in model.products)
    return total_conversions

def calculate_total_leads(model):
    '''
    This function calculates the total expected conversions.

    Parameters
    ----------
    model : Pyomo ConcreteModel
        The optimization model.

    Return
    ------------
    double
        Total expected leads.
    '''
    total_leads = sum(model.expected_leads[i] * model.y[i] for i in model.products)
    return total_leads

def calculate_total_risk_prod(model):
    '''
    This function calculates the total (linearized) risk of when planning the product investment.

    Parameters
    ----------
    model : Pyomo ConcreteModel
        The optimization model.

    Return
    ------------
    double
        Total risk.
    '''
    total_risk = sum(model.z[i,j] * model.covariance[i,j] for i in model.products for j in model.products)
    return total_risk

def calculate_total_risk_original(model):
    '''
    This function calculates the total (quadratic) risk of when planning the product investment.

    Parameters
    ----------
    model : Pyomo ConcreteModel
        The optimization model.

    Return
    ------------
    double
        Total risk.
    '''
    total_risk = sum(model.y[i] * model.y[j] * model.covariance[i,j] for i in model.products for j in model.products)
    return total_risk

def calculate_total_CPA(model):
    '''
    This function calculates the total expected CPA.

    Parameters
    ----------
    model : Pyomo ConcreteModel
        The optimization model.

    Return
    ------------
    double
        Total expected CPA.
    '''
    total_cpa = sum(model.expected_cpa[i] * model.y[i] for i in model.products)
    return total_cpa

def calculate_total_CPL(model):
    '''
    This function calculates the total expected CPL.

    Parameters
    ----------
    model : Pyomo ConcreteModel
        The optimization model.

    Return
    ------------
    double
        Total expected CPL.
    '''
    total_cpa = sum(model.expected_cpl[i] * model.y[i] for i in model.products)
    return total_cpa