# -*- coding: utf-8 -*-
"""
create_model.py
====================================
Function for the mathematical model (Sets, Parameters and Variables).

@author:
     - j.rodriguez.villegas
"""

from pyomo.environ import *

def create_marketing_model(product_media_data, product_data, media_data, covariance_data):
    '''
    Create a marketing media optimization model.

    Parameters
    ----------
    product_media_data : DataFrame
        Data containing conversion rates, lead rates, click rates, etc.
    product_data : DataFrame
        Data containing product-specific information.
    media_data : DataFrame
        Data containing media-specific information.

    Returns
    -------
    ConcreteModel
        The created Pyomo ConcreteModel for marketing media optimization.
    '''

    # Create a Pyomo ConcreteModel
    model = ConcreteModel('marketing_budget')

    # Extract unique products and media
    unique_products = product_data['ID'].drop_duplicates()
    medios_filtrados = media_data['ID'].drop_duplicates()

    # Define Sets
    model.products = Set(initialize=unique_products)
    model.media = Set(initialize=medios_filtrados)

    # Define Parameters
    model.conversion_rate = Param(model.products, model.media, initialize = product_media_data.set_index(['Producto', 'Medio'])['Tasa_Conversiones'].to_dict())
    model.lead_rate = Param(model.products, model.media, initialize = product_media_data.set_index(['Producto', 'Medio'])['Tasa_Leads'].to_dict())
    model.click_rate = Param(model.products, model.media, initialize = product_media_data.set_index(['Producto', 'Medio'])['Tasa_Clicks'].to_dict())
    model.cost_per_adquisition = Param(model.products, model.media, initialize = product_media_data.set_index(['Producto', 'Medio'])['CPA'].to_dict())
    model.cost_per_lead = Param(model.products, model.media, initialize = product_media_data.set_index(['Producto', 'Medio'])['CPL'].to_dict())
    model.min_investment = Param(model.media, initialize = media_data.set_index('ID')['Inversion_min'].to_dict())
    model.max_investment = Param(model.media, initialize = media_data.set_index('ID')['Inversion_max'].to_dict())

    # Initialize other parameters as needed
    model.min_weight = Param(model.products, initialize=product_data.set_index('ID')['peso_min'].to_dict())
    model.max_weight = Param(model.products, initialize=product_data.set_index('ID')['peso_max'].to_dict())
    model.risk = Param(model.products, initialize=product_data.set_index('ID')['Riesgo'].to_dict())
    model.budget_per_product = Param(model.products, initialize=product_data.set_index('ID')['presupuesto'].to_dict())
    model.budget = Param(initialize=sum(model.budget_per_product[i] for i in model.products))
    model.expected_clicks = Param(initialize = 0)
    model.expected_conversions = Param(initialize = 10000)
    model.expected_leads = Param(initialize = 0)
    model.expected_cpa = Param(initialize = 5000)
    model.expected_cpl = Param(initialize = 9999999999999999999)

    # Define and initialize covariance parameter
    covariance_dict = {(i, j, k): covariance for (i, j, k, covariance) in covariance_data}
    model.covariance_media = Param(model.products, model.media, model.media, initialize = covariance_dict)

    # Define decision Variables
    model.x = Var(model.products, model.media, domain=NonNegativeReals)
    model.u = Var(model.products, model.media, model.media, domain=NonNegativeReals)

    return model

