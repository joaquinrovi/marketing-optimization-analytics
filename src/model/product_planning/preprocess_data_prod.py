# -*- coding: utf-8 -*-
"""
preprocess_data_prod.py
====================================
Functions to read, process and clean data.

@author:
     - j.rodriguez.villegas
"""
import pandas as pd

def read_data(file_path, sheet_name):
    '''
    Reads data from an Excel file into a DataFrame.

    Parameters
    ----------
    file_path : str
        The path to the Excel file.
    sheet_name : str
        The name of the sheet within the Excel file to read.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the data from the specified Excel sheet.
    '''
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df

def filter_prod_data(data, products):
    '''
    Filters data based on a list of products.

    Parameters
    ----------
    data : pd.DataFrame
        The input DataFrame.
    products : list
        List of products to filter.

    Returns
    -------
    pd.DataFrame
        A filtered DataFrame containing only the specified products and media platforms.
    '''
    filtered_data = data[data['Producto'].isin(products)]
    return filtered_data

def filter_prod_data_2(data, products):
    '''
    Filters data based on a list of products.

    Parameters
    ----------
    data : pd.DataFrame
        The input DataFrame.
    products : list
        List of products to filter.

    Returns
    -------
    pd.DataFrame
        A filtered DataFrame containing only the specified products and media platforms.
    '''
    filtered_data = data[data['ID'].isin(products)]
    return filtered_data

def create_pivot_table(df):
    '''
    Creates a pivot table from a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.

    Returns
    -------
    pd.DataFrame
        A pivot table with "Fecha" as the index, "Producto" as columns, and "Sum_resultado" as values.
    '''
    sum_results_df = df.groupby(["Fecha", "Producto"])["Resultado"].sum().reset_index()
    sum_results_df.rename(columns={"Resultado": "Sum_resultado"}, inplace=True)

    pivot_table = sum_results_df.pivot(index = "Fecha", columns = "Producto", values = "Sum_resultado")
    return pivot_table

def calculate_covariance_matrix(pivot_table):
    '''
    Calculates the covariance matrix from a pivot table.

    Parameters
    ----------
    pivot_table : pd.DataFrame
        The pivot table containing products conversions/leads.

    Returns
    -------
    pd.DataFrame
        The covariance matrix of product conversions/leads.
    '''
    covariance_matrix = pivot_table.cov()
    return covariance_matrix

def calculate_expected_conversions(df):
    '''
    Calculates the expected conversions for each product (if the objective is conversions).

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.

    Returns
    -------
    pd.DataFrame
        A DataFrame with product names and their corresponding mean (average) conversions.
    '''
    
    sum_results_df = df.groupby(["Fecha", "Producto"])["Conversiones"].sum().reset_index()
    sum_results_df.rename(columns={"Conversiones": "Sum_Conversiones"}, inplace=True)

    # Only consider positive values to avoid bias
    filtered_df = sum_results_df[sum_results_df["Sum_Conversiones"] > 0]

    products_df = filtered_df.groupby("Producto")["Sum_Conversiones"].mean().reset_index()
    products_df.rename(columns={"Sum_Conversiones": "Conversiones esperadas"}, inplace=True)

    # Create a DataFrame with all products and merge it with the result
    all_products = pd.DataFrame({'Producto': df['Producto'].unique()})
    result_df = pd.merge(all_products, products_df, on='Producto', how='left').fillna(0)

    return result_df

def calculate_expected_leads(df):
    '''
    Calculates the expected leads for each product (if the objective is leads).

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.

    Returns
    -------
    pd.DataFrame
        A DataFrame with product names and their corresponding mean (average) leads.
    '''
    
    sum_results_df = df.groupby(["Fecha", "Producto"])["Leads"].sum().reset_index()
    sum_results_df.rename(columns={"Leads": "Sum_Leads"}, inplace=True)

    # Only consider positive values to avoid bias
    filtered_df = sum_results_df[sum_results_df["Sum_Leads"] > 0]

    products_df = filtered_df.groupby("Producto")["Sum_Leads"].mean().reset_index()
    products_df.rename(columns={"Sum_Leads": "Leads esperados"}, inplace=True)

    # Create a DataFrame with all products and merge it with the result
    all_products = pd.DataFrame({'Producto': df['Producto'].unique()})
    result_df = pd.merge(all_products, products_df, on='Producto', how='left').fillna(0)

    return result_df

def calculate_expected_cpa(df):
    '''
    Calculates the expected cpa for each product.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.

    Returns
    -------
    pd.DataFrame
        A DataFrame with product names and their corresponding mean (average) CPA.
    '''
    
    sum_CPA_df = df.groupby(["Fecha", "Producto"])["CPA"].sum().reset_index()
    sum_CPA_df.rename(columns={"CPA": "Sum_CPA"}, inplace=True)

    # Only consider positive values to avoid bias
    filtered_df = sum_CPA_df[sum_CPA_df["Sum_CPA"] > 0]

    products_df = filtered_df.groupby("Producto")["Sum_CPA"].mean().reset_index()
    products_df.rename(columns={"Sum_CPA": "CPA esperado"}, inplace=True)

    # Create a DataFrame with all products and merge it with the result
    all_products = pd.DataFrame({'Producto': df['Producto'].unique()})
    result_df = pd.merge(all_products, products_df, on='Producto', how='left').fillna(0)

    return result_df

def calculate_expected_cpl(df):
    '''
    Calculates the expected cpl for each product.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.

    Returns
    -------
    pd.DataFrame
        A DataFrame with product names and their corresponding mean (average) CPL.
    '''
    
    sum_CPL_df = df.groupby(["Fecha", "Producto"])["CPL"].sum().reset_index()
    sum_CPL_df.rename(columns={"CPL": "Sum_CPL"}, inplace=True)

    # Only consider positive values to avoid bias
    filtered_df = sum_CPL_df[sum_CPL_df["Sum_CPL"] > 0]

    products_df = filtered_df.groupby("Producto")["Sum_CPL"].mean().reset_index()
    products_df.rename(columns={"Sum_CPL": "CPL esperado"}, inplace=True)

    # Create a DataFrame with all products and merge it with the result
    all_products = pd.DataFrame({'Producto': df['Producto'].unique()})
    result_df = pd.merge(all_products, products_df, on='Producto', how='left').fillna(0)

    return result_df