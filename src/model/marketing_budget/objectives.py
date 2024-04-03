# -*- coding: utf-8 -*-
"""
objetives.py
====================================
Functions for the objectives of the mathematical model.

@author:
     - j.rodriguez.villegas
"""

from pyomo.environ import *

def create_objective(model):
    """Sets the model's objectives functions.

    Parameters
    ----------
    model : Pyomo ConcreteModel
        The optimization model.
    Returns
    -------
    Pyomo ConcreteModel
        The optimization model.
    """
    model.obj_funct_aggregated = Objective(sense = maximize, rule = aggregated_objective)
    return model

# Multi-objetive functions
weight_total_conversions = 1 # For now, conversions and CPA are given the same weight
weight_total_cpa = 0
weight_total_clicks = 0
weight_total_cpl = 0
weight_total_leads = 0

def aggregated_objective(model):
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
        weight_total_conversions * calculate_total_conversions(model) + 
        weight_total_cpa * calculate_total_cost_per_adquisition(model) + 
        weight_total_clicks * calculate_total_clicks(model) +
        weight_total_leads * calculate_total_leads(model) + 
        weight_total_cpl * calculate_total_cost_per_lead(model)
    )

# Maximization functions

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
    total_conversions = sum(model.conversion_rate[i,j] * model.x[i,j] for i in model.products for j in model.media)
    return total_conversions

def calculate_total_leads(model):
    '''
    This function calculates the total expected leads.

    Parameters
    ----------
    model : Pyomo ConcreteModel
        The optimization model.

    Return
    ------------
    double
        Total expected leads.
    '''
    total_leads = sum(model.lead_rate[i,j] * model.x[i,j] for i in model.products for j in model.media)
    return total_leads

def calculate_total_clicks(model):
    '''
    This function calculates the total expected clicks.

    Parameters
    ----------
    model : Pyomo ConcreteModel
        The optimization model.

    Return
    ------------
    double
        Total expected clicks.
    '''
    total_clicks = sum(model.click_rate[i,j] * model.x[i,j] for i in model.products for j in model.media)
    return total_clicks


# Minimization functions

def calculate_total_cost_per_adquisition(model):
    '''
    This function calculates the total expected general cost per adquisition.

    Parameters
    ----------
    model : Pyomo ConcreteModel
        The optimization model.

    Return
    ------------
    double
        Total estimated cost per adquisition.
    '''
    total_cpa = sum(model.cost_per_adquisition[i,j] * model.x[i,j] / model.budget for i in model.products for j in model.media)
    return total_cpa

def calculate_total_cost_per_lead(model):
    '''
    This function calculates the total expected general cost per lead.

    Parameters
    ----------
    model : Pyomo ConcreteModel
        The optimization model.

    Return
    ------------
    double
        Total estimated cost per lead.
    '''
    total_cpl = sum(model.cost_per_lead[i,j] * model.x[i,j] / model.budget for i in model.products for j in model.media)
    return total_cpl
