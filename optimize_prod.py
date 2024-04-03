# -*- coding: utf-8 -*-
"""
optimize_prod.py
====================================
Run the optimizer (get the best recommendations for product planning).

@author:
     - j.rodriguez.villegas
"""

from pyomo.environ import SolverFactory, SolverStatus, TerminationCondition

from src.model.product_planning.preprocess_data_prod import *
from src.model.product_planning.create_model_prod import *
from src.model.product_planning.constraints_prod import *
from src.model.product_planning.objectives_prod import *
from src.model.product_planning.generate_output_prod import *

if __name__ == "__main__":
    # Specify the path to the configuration file
    file_path = '../01_data/configuration_file_general_new.xlsx' # Change the path
    historic_sheet_name = 'Historic'
    productos_sheet_name = 'Productos'
    
    # Load data and create the optimization model
    historic_raw_data = read_data(file_path, historic_sheet_name)
    product_raw_data = read_data(file_path, productos_sheet_name)

    # Select the products of preference
    productos_filtrados = ["asd_auto", "asd_moto", "credito_auto", "credito_hipotecario", "double_play", "adelanto_sueldo",
                           "portabilidad", "credito_pyme", "credito_nomina", "ilc", "ppi", "credito_auto", "seguro_vida",
                           "fondos_actuales", "fondos_nuevos", "cuenta_digital", "seguro_estudia", "plazos_nuevos", "plazos_actuales", 
                           "efi", "seguro_cirugia", "seguro_hogar", "tdc_bbdd", "seguro_mascotas", "seguro embarazo"] # At least 2 otherwise it won't work

    filtered_product_data = filter_prod_data_2(product_raw_data, productos_filtrados)
    filtered_historic_prod_data = filter_prod_data(historic_raw_data, productos_filtrados)
    conversions_data = calculate_expected_conversions(filtered_historic_prod_data)
    leads_data = calculate_expected_leads(filtered_historic_prod_data)
    cpa_data = calculate_expected_cpa(filtered_historic_prod_data)
    cpl_data = calculate_expected_cpl(filtered_historic_prod_data)
    pivot_table = create_pivot_table(filtered_historic_prod_data)
    covariance_matrix = calculate_covariance_matrix(pivot_table)
    model = create_optimization_model(conversions_data, leads_data, cpa_data, cpl_data, filtered_product_data, covariance_matrix)

    # Create constraints and objective
    create_contraints(model)
    create_objective(model)

    # Solve the optimization model

    print('# PROCESSING MODEL #')
    print('# OPTIMIZING PRODUCT PLANNING #')

    solver = SolverFactory('glpk')
    solver.options['tmlim'] = 600
    result = solver.solve(model, tee=True, report_timing=True)

    # Check the solver's termination condition
    termination_condition = result.solver.termination_condition
    solver_status = result.solver.status

    # Print the results or handle them accordingly
    if solver_status == SolverStatus.ok and termination_condition == TerminationCondition.optimal:
        print("Optimal solution found.")
        total_expected_leads = value(calculate_total_leads(model))
        total_expected_conversions = value(calculate_total_conversions(model))
        total_risk = value(calculate_total_risk_prod(model))
        total_expected_CPA = value(calculate_total_CPA(model))
        total_expected_CPL = value(calculate_total_CPL(model))
        print("Total Expected leads:", total_expected_leads)
        print("Total Expected conversions:", total_expected_conversions)
        print("Total Expected CPA:", total_expected_CPA)
        print("Total Expected CPL:", total_expected_CPL)
    else:
        print("No optimal solution found or other solver issues...")
        print("Solver terminated with condition:", solver_status)


    # Export results
    output_file = '../03_output/results_optimizer_product.xlsx'  # Output file path

    results = collect_results_prod(model)

    export_results_to_excel_prod(results, output_file)
