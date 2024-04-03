# -*- coding: utf-8 -*-
"""
optimize.py
====================================
Run the optimizer (get the best recommendations for marketing investment).

@author:
     - j.rodriguez.villegas
"""

from pyomo.environ import SolverFactory, SolverStatus, TerminationCondition

from src.model.marketing_budget.preprocess_data import *
from src.model.marketing_budget.create_model import *
from src.model.marketing_budget.objectives import *
from src.model.marketing_budget.constraints import *
from src.model.marketing_budget.generate_output import *

if __name__ == "__main__":
    # Load data
    config_file_url = '../01_data/configuration_file_general_new.xlsx' # Change the path
    
    mix_sheet_name = 'Mix'
    productos_sheet_name = 'Productos'
    medios_sheet_name = 'Medios'
    historic_sheet_name = 'Historic'
    
    product_media_raw_data = read_configuration_data(config_file_url, mix_sheet_name)
    product_raw_data = read_configuration_data(config_file_url, productos_sheet_name)
    media_raw_data = read_configuration_data(config_file_url, medios_sheet_name)
    historic_raw_data = read_configuration_data(config_file_url, historic_sheet_name)

    # Select the product of preference
    productos_filtrados = ["double_play"]

    # Select the media platforms of preference
    medios_filtrados = ["Amazon", "DV360", "Facebook", "Google Display Network", 
                        "Google Search Ads", "Medios Terceros", "Performance Max", "Rocket", "TikTok", "Zoom D"]
    
    # Apply filters
    filtered_product_media_data = filter_product_media_data(product_media_raw_data, productos_filtrados, medios_filtrados)
    filtered_product_data = filter_product_data(product_raw_data, productos_filtrados)
    filtered_media_data = filter_media_data(media_raw_data, medios_filtrados)
    filtered_historic_data = filter_data(historic_raw_data, productos_filtrados, medios_filtrados)
    pivot_df = filtered_historic_data.pivot(index=["Producto", "Fecha"], columns="Medio", values="Resultado").reset_index()
    unique_products = pivot_df["Producto"].unique()
    covariance_matrix = calculate_covariances(pivot_df, unique_products, medios_filtrados)

    # Create optimization model

    model = create_marketing_model(filtered_product_media_data, filtered_product_data, filtered_media_data, covariance_matrix)
    create_objective(model)
    create_contraints(model)

    # Solve the optimization model

    print('# PROCESSING MODEL #')
    print('# OPTIMIZING MARKETING BUDGET #')

    solver = SolverFactory('glpk')
    solver.options['tmlim'] = 600
    result = solver.solve(model, tee=True, report_timing=True)

    # Check the solver's termination condition
    termination_condition = result.solver.termination_condition
    solver_status = result.solver.status

    if solver_status == SolverStatus.ok and termination_condition == TerminationCondition.optimal:
          print("Optimal solution found.")
          total_expected_conversions = value(calculate_total_conversions(model))
          total_expected_cpa = value(calculate_total_cost_per_adquisition(model))
          print("Total expected conversions:", total_expected_conversions)
          print("Total expected CPA:", total_expected_cpa)
    else:
          print("No optimal solution found or other solver issues...")
          print("Solver terminated with condition:", solver_status)

    # Export results
    output_file = '../03_output/results_optimizer_general.xlsx'  # Output file path

    results = collect_results(model)
    budget = value(model.budget)

    export_results_to_excel(results, budget, output_file)