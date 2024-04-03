# -*- coding: utf-8 -*-
"""
generate_output.py
====================================
Create the necessary functions in order to export the results of the optimization model.

@author:
     - j.rodriguez.villegas
"""

import pandas as pd

def collect_results(model):
    '''
    This function collects optimization results from the Pyomo model and organizes them into a list of tuples. 
    The results include information related to the allocation of resources to marketing media platforms and 
    various performance metrics for each combination of product and media.

    Parameters
    ----------
    model : Pyomo ConcreteModel
        The Pyomo model containing Decision Variables, Parameters, and Sets related to the optimization problem.

    Returns
    -------
    results : list of tuples
        A list of tuples where each tuple contains information related to resource allocation 
        and performance metrics for each product and media combination.
    '''
    results = []

    for i in model.products:
        for j in model.media:
            value = model.x[i, j].value
            percentage = value / model.budget
            conversion_rate = model.conversion_rate[i, j]
            lead_rate = model.lead_rate[i, j]
            cpa = model.cost_per_adquisition[i, j]
            click_rate = model.click_rate[i, j]
            obj_value_leads = model.lead_rate[i, j] * value
            obj_value_CPL = model.cost_per_lead[i, j] * percentage
            obj_value_conversion = model.conversion_rate[i, j] * value
            obj_value_CPA = model.cost_per_adquisition[i, j] * percentage
            obj_value_clicks = model.click_rate[i, j] * value
            results.append((i, j, value, percentage, conversion_rate, lead_rate, cpa, click_rate ,obj_value_leads, obj_value_CPL, obj_value_conversion, obj_value_CPA, obj_value_clicks))
    
    return results

def export_results_to_excel(results, budget, output_file):
    '''
    Exports optimization results to an Excel file.

    Parameters
    ----------
    results : list
        A list containing optimization results for decision variable x.
    budget : float
        The total budget used in the optimization.
    output_file : str
        The path to the output Excel file.
    '''

    # Create a DataFrame from the results list
    df_decisions = pd.DataFrame(results, columns=['Producto', 'Medio', 'Inversion', 'Porcentaje', 'Tasa de conversiones', 'Tasa de Leads', 'CPA unitario', 'Tasa de clicks', 'Leads esperados', 'CPL esperado', 'Conversiones esperadas', 'CPA esperado', 'Clicks esperados'])

    # Create a DataFrame for the objective value
    df_objective = pd.DataFrame({'Presupuesto del mes': [budget]})

    # Export the DataFrames to an Excel file with two sheets
    with pd.ExcelWriter(output_file) as writer:
        df_decisions.to_excel(writer, sheet_name='Decisiones optimas', index=False)
        df_objective.to_excel(writer, sheet_name='Presupuesto', index=False)