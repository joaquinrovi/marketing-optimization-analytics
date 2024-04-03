# -*- coding: utf-8 -*-
"""
preprocess_data.py
====================================
Functions to read, process and clean data.

@author:
     - j.rodriguez.villegas
"""

import numpy as np
import pandas as pd

def read_configuration_data(file_path, sheet_name):
    '''
    Reads data from a configuration file into a DataFrame.

    Parameters
    ----------
    file_path : str
        The path to the Excel configuration file.
    sheet_name : str
        The name of the sheet within the Excel file to read.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the data from the specified sheet in the configuration file.
    '''
    data = pd.read_excel(file_path, sheet_name=sheet_name)
    return data

def filter_product_media_data(product_media_data, products, media):
    '''
    Filters product and media data based on lists of products and media platforms.

    Parameters
    ----------
    product_media_data : pd.DataFrame
        The input DataFrame containing product and media data.
    products : list
        List of products to filter.
    media : list
        List of media platforms to filter.

    Returns
    -------
    pd.DataFrame
        A filtered DataFrame containing only the specified products and media platforms.
    '''
    filtered_data = product_media_data[(product_media_data['Producto'].isin(products)) & (product_media_data['Medio'].isin(media))]
    return filtered_data

def filter_product_data(product_data, products):
    '''
    Filters product data based on a list of products.

    Parameters
    ----------
    product_data : pd.DataFrame
        The input DataFrame containing product data.
    products : list
        List of products to filter.

    Returns
    -------
    pd.DataFrame
        A filtered DataFrame containing only the specified products.
    '''
    filtered_data = product_data[product_data['ID'].isin(products)]
    return filtered_data

def filter_media_data(media_data, media):
    '''
    Filters media data based on a list of media platforms.

    Parameters
    ----------
    media_data : pd.DataFrame
        The input DataFrame containing media data.
    media : list
        List of media platforms to filter.

    Returns
    -------
    pd.DataFrame
        A filtered DataFrame containing only the specified media platforms.
    '''
    filtered_data = media_data[media_data['ID'].isin(media)]
    return filtered_data

def filter_data(historical_data, products, media):
    '''
    Filters data based on a list of products and media platforms.

    Parameters
    ----------
    historical_data : pd.DataFrame
        The input DataFrame.
    products : list
        List of products to filter.
    media : list
        List of media platforms to filter.

    Returns
    -------
    pd.DataFrame
        A filtered DataFrame containing only the specified products and media platforms.
    '''
    filtered_data = historical_data[(historical_data['Producto'].isin(products)) & (historical_data['Medio'].isin(media))]
    return filtered_data


def calculate_covariances(pivot_data, products, media):
    '''
    Calculates covariances for different combinations of media platforms within each product.

    Parameters
    ----------
    pivot_data : pd.DataFrame
        The pivot table DataFrame.
    products : list
        List of unique products.
    media : list
        List of media platforms.

    Returns
    -------
    list
        A list of tuples containing (product, media1, media2, covariance) for all combinations.
    '''
    covariances = []

    for product in products:
        product_df = pivot_data[pivot_data["Producto"] == product]
        media_covariances = []

        for media1 in media:
            for media2 in media:
                covariance = product_df[media1].cov(product_df[media2])
                media_covariances.append((product, media1, media2, covariance))

        covariances.extend(media_covariances)

    return covariances
