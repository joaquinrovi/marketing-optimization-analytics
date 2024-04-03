# -*- coding: utf-8 -*-
"""
create_model_prod.py
====================================
Function for the mathematical model (Sets, Parameters and Variables) (product planning).

@author:
     - j.rodriguez.villegas
"""
from pyomo.environ import *

def create_optimization_model(conversions_data, leads_data, cpa_data, cpl_data, weight_data, covariance_matrix):
    '''
    Create a product planning optimization model.

    Parameters
    ----------
    conversions_data : DataFrame
        A DataFrame containing product conversions data.
    leads_data : DataFrame
        A DataFrame containing product leads data.
    weight_data : DataFrame
        A DataFrame containing weight data, including individual product weights.
    cpa_data : DataFrame
        A DataFrame containing cpa data for individual products.
    cpl_data : DataFrame
        A DataFrame containing cpl data for individual products.
    covariance_matrix : DataFrame
        A DataFrame containing the covariance matrix of product results (conversion/leads).

    Returns
    -------
    ConcreteModel
        The created Pyomo ConcreteModel for product planning optimization.
    '''
    model = ConcreteModel('product_planning')
    
    # Extract products from the columns of the covariance_matrix DataFrame
    products = list(covariance_matrix.columns)
    
    model.products = Set(initialize=products)  # Use the products extracted from covariance_matrix
    
    model.conversions_level = Param(initialize = 20000)
    model.leads_level = Param(initialize = 0)
    model.cpa_level = Param(initialize = 9999999999999999999)
    model.cpl_level = Param(initialize = 9999999999999999999)
    model.risk_level = Param(initialize = 9999999999999999999)
    model.min_weight = Param(model.products, initialize = weight_data.set_index('ID')['peso_min'].to_dict())
    model.max_weight = Param(model.products, initialize = weight_data.set_index('ID')['peso_max'].to_dict())
    model.expected_conversions = Param(model.products, initialize = conversions_data.set_index('Producto')["Conversiones esperadas"].to_dict())
    model.expected_leads = Param(model.products, initialize = leads_data.set_index('Producto')["Leads esperados"].to_dict())
    model.expected_cpa = Param(model.products, initialize = cpa_data.set_index('Producto')["CPA esperado"].to_dict())
    model.expected_cpl = Param(model.products, initialize = cpl_data.set_index('Producto')["CPL esperado"].to_dict())

    # Define and initialize covariance parameter
    covariance_dict = {(i, j): covariance_matrix.at[i, j] for i in products for j in products}
    model.covariance = Param(model.products, model.products, initialize=covariance_dict)

    model.y = Var(model.products, domain=NonNegativeReals, bounds=(0,1))
    model.z = Var(model.products, model.products, domain=NonNegativeReals)
    
    return model