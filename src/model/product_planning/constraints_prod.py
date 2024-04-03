# -*- coding: utf-8 -*-
"""
constraints_prod.py
====================================
Functions for the constraints of the mathematical model (product planning).

@author:
     - j.rodriguez.villegas
"""
from pyomo.environ import *

def create_contraints(model):
    model.c_1_weights = Constraint(rule=c_1_weights)
    model.c_2_1_conversions = Constraint(rule=c_2_1_conversions)
    model.c_2_2_leads = Constraint(rule=c_2_2_leads)
    model.c_3_1_linearized_risk = Constraint(rule=c_3_1_linearized_risk)
    model.c_3_2_linearized_risk = Constraint(model.products, model.products, rule=c_3_2_linearized_risk)
    model.c_3_3_linearized_risk = Constraint(model.products, model.products, rule=c_3_3_linearized_risk)
    model.c_3_4_linearized_risk = Constraint(model.products, model.products, rule=c_3_4_linearized_risk)
    model.c_4_non_negative = Constraint(model.products, rule = c_4_non_negative)
    model.c_5_min_weight = Constraint(model.products, rule = c_5_min_weight)
    model.c_5_1_max_weight = Constraint(model.products, rule = c_5_1_max_weight)
    model.c_6_cpa_product = Constraint(rule=c_6_cpa_product)
    model.c_7_cpa_product = Constraint(rule=c_7_cpl_product)

def c_1_weights(model):
    '''
    Ensures the total weight sums up to one.

    Parameters
    ----------
    model : Pyomo ConcreteModel
        The optimization model.

    Returns
    -------
    Constraint Expression
        Relational expression for the constraint.
    '''
    weight_left = sum(model.y[i] for i in model.products)
    weight_right = 1
    weight = (weight_left == weight_right)
    return weight

def c_2_1_conversions(model):
    '''
    Ensures the desired level of conversions in the product planning is accomplished

    Parameters
    ----------
    model : Pyomo ConcreteModel
        The optimization model.

    Returns
    -------
    Constraint Expression
        Relational expression for the constraint.
    '''
    expected_conversions_left = sum(model.expected_conversions[i] * model.y[i] for i in model.products)
    expected_conversions_right = model.conversions_level
    expected_conversions = (expected_conversions_left >= expected_conversions_right)
    return expected_conversions

def c_2_2_leads(model):
    '''
    Ensures the desired level of leads in the product planning is accomplished

    Parameters
    ----------
    model : Pyomo ConcreteModel
        The optimization model.

    Returns
    -------
    Constraint Expression
        Relational expression for the constraint.
    '''
    expected_leads_left = sum(model.expected_leads[i] * model.y[i] for i in model.products)
    expected_leads_right = model.leads_level
    expected_leads = (expected_leads_left >= expected_leads_right)
    return expected_leads

def c_3_risk(model):
    '''
    Original quadratic constraint to measure risk across the investment.

    Parameters
    ----------

    model : Pyomo ConcreteModel
        The optimization model.

    Returns
    -------
    Constraint Expression
        Relational expression for the constraint.
    '''
    risk_left = sum(model.y[i] * model.y[j] * model.covariance[i,j] for i in model.products for j in model.products)
    risk_right = model.risk_level
    risk = (risk_left <= risk_right)
    return risk

def c_3_1_linearized_risk(model):
    '''
    Linearizes the quadratic constraint by introducing an auxiliary variable.

    Parameters
    ----------

    model : Pyomo ConcreteModel
        The optimization model.

    Returns
    -------
    Constraint Expression
        Relational expression for the constraint.
    '''
    auxiliary_1_left = sum(model.z[i,j] * model.covariance[i,j] for i in model.products for j in model.products)
    auxiliary_1_right = model.risk_level
    auxiliary_1 = (auxiliary_1_left <= auxiliary_1_right)
    return auxiliary_1

def c_3_2_linearized_risk(model, i, j):
    '''
    Assigns bounds to the auxiliary variable for the linear convex relaxation (McCormick Envelopes).

    Parameters
    ----------

    model : Pyomo ConcreteModel
        The optimization model.
    i : string
        The assets.
    j : string.
        The assets.

    Returns
    -------
    Constraint Expression
        Relational expression for the constraint.
    '''
    lowBound = 0
    auxiliary_2_left = model.z[i,j]
    auxiliary_2_right = lowBound * model.y[j] + model.y[i] * lowBound  -  lowBound * lowBound
    auxiliary_2 = (auxiliary_2_left >= auxiliary_2_right)
    return auxiliary_2

def c_3_3_linearized_risk(model, i, j):
    '''
    Assigns bounds to the auxiliary variable for the linear convex relaxation (McCormick Envelopes).

    Parameters
    ----------

    model : Pyomo ConcreteModel
        The optimization model.
    i : string
        The assets.
    j : string.
        The assets.

    Returns
    -------
    Constraint Expression
        Relational expression for the constraint.
    '''
    upperBound = 1
    auxiliary_3_left = model.z[i,j]
    auxiliary_3_right = upperBound * model.y[j] + model.y[i] * upperBound  -  upperBound * upperBound
    auxiliary_3 = (auxiliary_3_left >= auxiliary_3_right)
    return auxiliary_3

def c_3_4_linearized_risk(model, i, j):
    '''
    Assigns bounds to the auxiliary variable for the linear convex relaxation (McCormick Envelopes).

    Parameters
    ----------

    model : Pyomo ConcreteModel
        The optimization model.
    i : string
        The assets.
    j : string.
        The assets.

    Returns
    -------
    Constraint Expression
        Relational expression for the constraint.
    '''
    lowBound = 0
    upperBound = 1
    auxiliary_4_left = model.z[i,j]
    auxiliary_4_right = upperBound * model.y[j] + model.y[i] * lowBound  -  upperBound * lowBound
    auxiliary_4 = (auxiliary_4_left <= auxiliary_4_right)
    return auxiliary_4

def c_3_5_linearized_risk(model, i, j):
    '''
    Assigns bounds to the auxiliary variable for the linear convex relaxation (McCormick Envelopes).

    Parameters
    ----------

    model : Pyomo ConcreteModel
        The optimization model.
    i : string
        The assets.
    j : string.
        The assets.

    Returns
    -------
    Constraint Expression
        Relational expression for the constraint.
    '''
    lowBound = 0
    upperBound = 1
    auxiliary_5_left = model.z[i,j]
    auxiliary_5_right = model.y[i] * upperBound  + lowBound * model.y[j]  -  lowBound * upperBound
    auxiliary_5 = (auxiliary_5_left <= auxiliary_5_right)
    return auxiliary_5

def c_4_non_negative(model, i):
    '''
    Non negativity in the decision variable.

    Parameters
    ----------

    model : Pyomo ConcreteModel
        The optimization model.
    i : string
        The assets.
    j : string.
        The assets.

    Returns
    -------
    Constraint Expression
        Relational expression for the constraint.
    '''
    non_negative_left = model.y[i]
    non_negative_right = 0
    non_negative = (non_negative_left >= non_negative_right)
    return non_negative

def c_5_min_weight(model,i):
    '''
    Ensures each product has a minimum importance weight.

    Parameters
    ----------
    model : Pyomo ConcreteModel
        The optimization model.
    i : string
        The products.    

    Returns
    -------
    Constraint Expression
        Relational expression for the constraint.
    '''
    min_weight_left = model.y[i]
    min_weight_right = model.min_weight[i] 
    min_weight = (min_weight_left >= min_weight_right)
    return min_weight

def c_5_1_max_weight(model,i):
    '''
    Ensures each product has a maximum importance weight.

    Parameters
    ----------
    model : Pyomo ConcreteModel
        The optimization model.
    i : string
        The products.    

    Returns
    -------
    Constraint Expression
        Relational expression for the constraint.
    '''
    max_weight_left = model.y[i]
    max_weight_right = model.max_weight[i] 
    max_weight = (max_weight_left <= max_weight_right)
    return max_weight

def c_6_cpa_product(model):
    '''
    Ensures the maximum permited CPA level in the product planning is accomplished

    Parameters
    ----------
    model : Pyomo ConcreteModel
        The optimization model.

    Returns
    -------
    Constraint Expression
        Relational expression for the constraint.
    '''
    expected_cpa_left = sum(model.expected_cpa[i] * model.y[i] for i in model.products)
    expected_cpa_right = model.cpa_level
    expected_cpa = (expected_cpa_left <= expected_cpa_right)
    return expected_cpa

def c_7_cpl_product(model):
    '''
    Ensures the maximum permited CPL level in the product planning is accomplished

    Parameters
    ----------
    model : Pyomo ConcreteModel
        The optimization model.

    Returns
    -------
    Constraint Expression
        Relational expression for the constraint.
    '''
    expected_cpl_left = sum(model.expected_cpl[i] * model.y[i] for i in model.products)
    expected_cpl_right = model.cpl_level
    expected_cpl = (expected_cpl_left <= expected_cpl_right)
    return expected_cpl