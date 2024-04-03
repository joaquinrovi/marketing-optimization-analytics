# -*- coding: utf-8 -*-
"""
generate_output.py
====================================
Create the necessary functions in order to export the results of the optimization model.

@author:
     - j.rodriguez.villegas
"""

import pandas as pd

def collect_results_prod(model):
    '''
    This function collects optimization results from the Pyomo model and organizes them into a list of tuples. 
    The results include information related to investment product planning and various performance metrics 
    for each product.

    Parameters
    ----------
    model : Pyomo ConcreteModel
        The Pyomo model containing Decision Variables, Parameters, and Sets related to the optimization problem.

    Returns
    -------
    results : list of tuples
        A list of tuples where each tuple contains information related to product planning 
        and performance metrics for each product.
    '''
    results = []

    for i in model.products:
        percentage = model.y[i].value
        obj_value_leads = model.expected_leads[i] * percentage
        obj_value_conversions = model.expected_conversions[i] * percentage
        obj_value_cpa = model.expected_cpa[i] * percentage
        obj_value_cpl = model.expected_cpl[i] * percentage
        results.append((i, percentage, obj_value_leads, obj_value_conversions, obj_value_cpa, obj_value_cpl))
    return results

def export_results_to_excel_prod(results, output_file):
    '''
    Exports optimization results to an Excel file.

    Parameters
    ----------
    results : list
        A list containing optimization results for decision variable y.
    output_file : str
        The path to the output Excel file.
    '''

    # Create a DataFrame from the results list
    df_decisions = pd.DataFrame(results, columns=['Producto', 'Porcentaje', 'Leads esperados', 'Conversiones esperadas', 'CPA esperado', 'CPL esperado'])

    # Export the DataFrames to an Excel file with two sheets
    with pd.ExcelWriter(output_file) as writer:
        df_decisions.to_excel(writer, sheet_name='Decisiones optimas', index=False)