# -*- coding: utf-8 -*-
"""
constraints.py
====================================
Functions for the constraints of the mathematical model.

@author:
     - j.rodriguez.villegas
"""
from pyomo.environ import *

def create_contraints(model):
    '''
    Adds all the necessary constraints in the optimization model.

    Parameters
    ----------
    model : Pyomo ConcreteModel
        The optimization model.

    Returns
    -------
    Pyomo ConcreteModel
        The optimization model.
    '''
    model.c_1_budget = Constraint(rule=c_1_budget)
    model.c_2_min_investment = Constraint(model.media, rule=c_2_min_investment)
    model.c_3_max_investment = Constraint(model.media, rule=c_3_max_investment)
    model.c_4_min_weight = Constraint(model.products, rule = c_4_min_weight)
    model.c_5_min_number_of_clicks = Constraint(rule = c_5_min_number_of_clicks)
    model.c_6_min_number_of_conversions = Constraint(rule = c_6_min_number_of_conversions)
    model.c_7_min_number_of_leads = Constraint(rule = c_7_min_number_of_leads)
    model.c_8_max_cost_per_adquisition = Constraint(rule = c_8_max_cost_per_adquisition)
    model.c_9_max_cost_per_lead = Constraint(rule = c_9_max_cost_per_lead)
    model.c_10_1_auxiliary_linearization = Constraint(model.products, rule = c_10_1_auxiliary_linearization)
    model.c_10_2_auxiliary_linearization = Constraint(model.products, model.media, model.media, rule = c_10_2_auxiliary_linearization)
    model.c_10_3_auxiliary_linearization = Constraint(model.products, model.media, model.media, rule = c_10_3_auxiliary_linearization)
    model.c_10_4_auxiliary_linearization = Constraint(model.products, model.media, model.media, rule = c_10_4_auxiliary_linearization)
    model.c_10_5_auxiliary_linearization = Constraint(model.products, model.media, model.media, rule = c_10_5_auxiliary_linearization)
    model.c_11_non_negative_constraint = Constraint(model.products, model.media, rule = c_11_non_negative_constraint)
    return model

def c_1_budget(model):
    '''
    Ensures the marketing budget is satisfied for all products and media platforms.

    Parameters
    ----------
    model : Pyomo ConcreteModel
        The optimization model.

    Returns
    -------
    Constraint Expression
        Relational expression for the constraint.
    '''
    budget_left = sum(model.x[i,j] for i in model.products for j in model.media)
    budget_right = model.budget
    budget = (budget_left == budget_right)
    return budget

def c_2_min_investment(model,j):
    '''
    Ensures that there is a minimum investment on each media platform.

    Parameters
    ----------
    model : Pyomo ConcreteModel
        The optimization model.
    j : string
        The media platforms.    

    Returns
    -------
    Constraint Expression
        Relational expression for the constraint.
    '''
    min_investment_left = sum(model.x[i,j] for i in model.products)
    min_investment_right = model.min_investment[j] 
    min_investment = (min_investment_left >= min_investment_right)
    return min_investment

def c_3_max_investment(model,j):
    '''
    Ensures that there is a maximum investment on each media platform.

    Parameters
    ----------
    model : Pyomo ConcreteModel
        The optimization model.
    j : string
        The media platforms.  

    Returns
    -------
    Constraint Expression
        Relational expression for the constraint.
    '''
    max_investment_left = sum(model.x[i,j] for i in model.products)
    max_investment_right = model.max_investment[j] 
    max_investment = (max_investment_left <= max_investment_right)
    return max_investment

def c_4_min_weight(model,i):
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
    min_weight_left = sum(model.x[i,j] / model.budget for j in model.media)
    min_weight_right = model.min_weight[i] 
    min_weight = (min_weight_left >= min_weight_right)
    return min_weight

def c_4_1_max_weight(model,i):
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
    max_weight_left = sum(model.x[i,j] / model.budget for j in model.media)
    max_weight_right = model.max_weight[i] 
    max_weight = (max_weight_left <= max_weight_right)
    return max_weight

def c_5_min_number_of_clicks(model):
    '''
    Ensures the minimum total number of clicks is satisfied.

    Parameters
    ----------

    model : Pyomo ConcreteModel
        The optimization model.

    Returns
    -------
    Constraint Expression
        Relational expression for the constraint.
    '''
    clicks = model.expected_clicks
    min_clicks_left = sum(model.click_rate[i,j] * model.x[i,j] for i in model.products for j in model.media)
    min_clicks_right = clicks
    min_clicks = (min_clicks_left >= min_clicks_right)
    return min_clicks

def c_6_min_number_of_conversions(model):
    '''
    Ensures the minimum total number of conversions is satisfied.

    Parameters
    ----------

    model : Pyomo ConcreteModel
        The optimization model.

    Returns
    -------
    Constraint Expression
        Relational expression for the constraint.
    '''
    conversions = model.expected_conversions
    min_conversions_left = sum(model.conversion_rate[i,j] * model.x[i,j] for i in model.products for j in model.media)
    min_conversions_right = conversions
    min_conversions = (min_conversions_left >= min_conversions_right)
    return min_conversions

def c_7_min_number_of_leads(model):
    '''
    Ensures the minimum total number of leads is satisfied.

    Parameters
    ----------

    model : Pyomo ConcreteModel
        The optimization model.

    Returns
    -------
    Constraint Expression
        Relational expression for the constraint.
    '''
    leads = model.expected_leads
    min_leads_left = sum(model.lead_rate[i,j] * model.x[i,j] for i in model.products for j in model.media)
    min_leads_right = leads
    min_leads = (min_leads_left >= min_leads_right)
    return min_leads

def c_8_max_cost_per_adquisition(model):
    '''
    Ensures the maximum total global CPA is permitted.

    Parameters
    ----------

    model : Pyomo ConcreteModel
        The optimization model.

    Returns
    -------
    Constraint Expression
        Relational expression for the constraint.
    '''
    CPA = model.expected_cpa
    max_cpa_left = sum(model.cost_per_adquisition[i,j] * model.x[i,j] / model.budget for i in model.products for j in model.media)
    max_cpa_right = CPA
    max_cpa = (max_cpa_left <= max_cpa_right)
    return max_cpa

def c_9_max_cost_per_lead(model):
    '''
    Ensures the maximum total global CPL is permitted.

    Parameters
    ----------

    model : Pyomo ConcreteModel
        The optimization model.

    Returns
    -------
    Constraint Expression
        Relational expression for the constraint.
    '''
    CPL = model.expected_cpl
    max_cpl_left = sum(model.cost_per_lead[i,j] * model.x[i,j] / model.budget for i in model.products for j in model.media)
    max_cpl_right = CPL
    max_cpl = (max_cpl_left <= max_cpl_right)
    return max_cpl

def c_10_quadratic_risk(model, i):
    '''
    Original quadratic constraint to reduce risk in the marketing investment (more precision).

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
    risk_left = sum(model.x[i,j] * model.x[i,k] * model.covariance_media[i,j,k] / model.budget for j in model.media for k in model.media)
    risk_right = model.risk[i]
    risk = (risk_left <= risk_right)
    return risk


def c_10_1_auxiliary_linearization(model, i):
    '''
    Linearizes the quadratic constraint by introducing an auxiliary variable.

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
    auxiliary_1_left = sum(model.u[i,j,k] * model.covariance_media[i,j,k] / model.budget for j in model.media for k in model.media)
    auxiliary_1_right = model.risk[i]
    auxiliary_1 = (auxiliary_1_left <= auxiliary_1_right)
    return auxiliary_1

def c_10_2_auxiliary_linearization(model, i, j, k):
    '''
    Assigns bounds to the auxiliary variable for the linear convex relaxation (McCormick Envelopes).

    Parameters
    ----------

    model : Pyomo ConcreteMode
        The optimization model.
    i : string
        The products.
    j : string.
        The media platforms.
    k : string.
        The media platforms.

    Returns
    -------
    Constraint Expression
        Relational expression for the constraint.
    '''
    lowBound = 0
    auxiliary_2_left = model.u[i,j,k]
    auxiliary_2_right = lowBound * model.x[i,k] + model.x[i,j] * lowBound  -  lowBound * lowBound
    auxiliary_2 = (auxiliary_2_left >= auxiliary_2_right)
    return auxiliary_2

def c_10_3_auxiliary_linearization(model, i, j, k):
    '''
    Assigns bounds to the auxiliary variable for the linear convex relaxation (McCormick Envelopes).

    Parameters
    ----------

    model : Pyomo ConcreteMode
        The optimization model.
    i : string
        The products.
    j : string.
        The media platforms.
    k : string.
        The media platforms.

    Returns
    -------
    Constraint Expression
        Relational expression for the constraint.
    '''
    upperBound = 9999999999
    auxiliary_3_left = model.u[i,j,k]
    auxiliary_3_right = upperBound * model.x[i,k] + model.x[i,j] * upperBound  -  upperBound * upperBound
    auxiliary_3 = (auxiliary_3_left >= auxiliary_3_right)
    return auxiliary_3

def c_10_4_auxiliary_linearization(model, i, j, k):
    '''
    Assigns bounds to the auxiliary variable for the linear convex relaxation (McCormick Envelopes).

    Parameters
    ----------

    model : Pyomo ConcreteMode
        The optimization model.
    i : string
        The products.
    j : string.
        The media platforms.
    k : string.
        The media platforms.

    Returns
    -------
    Constraint Expression
        Relational expression for the constraint.
    '''
    lowBound = 0
    upperBound = 9999999999
    auxiliary_4_left = model.u[i,j,k]
    auxiliary_4_right = upperBound * model.x[i,k] + model.x[i,j] * lowBound -  upperBound * lowBound
    auxiliary_4 = (auxiliary_4_left <= auxiliary_4_right)
    return auxiliary_4

def c_10_5_auxiliary_linearization(model, i, j, k):
    '''
    Assigns bounds to the auxiliary variable for the linear convex relaxation (McCormick Envelopes).

    Parameters
    ----------

    model : Pyomo ConcreteMode
        The optimization model.
    i : string
        The products.
    j : string.
        The media platforms.
    k : string.
        The media platforms.

    Returns
    -------
    Constraint Expression
        Relational expression for the constraint.
    '''
    lowBound = 0
    upperBound = 9999999999
    auxiliary_5_left = model.u[i,j,k]
    auxiliary_5_right = upperBound * model.x[i,j] + model.x[i,k] * lowBound -  upperBound * lowBound
    auxiliary_5 = (auxiliary_5_left <= auxiliary_5_right)
    return auxiliary_5

def c_11_non_negative_constraint(model,i,j):
    '''
    Ensures each decision variable is non negative.

    Parameters
    ----------

    model : Pyomo ConcreteModel
        The optimization model.
    i : string
        The products.
    j : string
        The media platforms.

    Returns
    -------
    Constraint Expression
        Relational expression for the constraint.
    '''
    non_negative = (model.x[i,j] >= 0)
    return non_negative