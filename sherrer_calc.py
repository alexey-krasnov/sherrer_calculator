#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from glob import glob
import sys
import numpy as np
import pandas as pd
from scipy.stats import t
import tabula


def read_table_from_pdf(pdf_name: str) -> pd.DataFrame:
    """Read a PDF File. Get DataFrame with data to process. It is the 1st table in the list of parsed tables"""
    dfs = tabula.io.read_pdf(pdf_name, pages='1', pandas_options={'header': None})
    return dfs[0]


def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    """Clean data in DataFrame. Get useful data of XRD measurement as '2Theta', 'd', 'I/I1', 'FWHM', 'Integrated Int'"""
    df.drop(labels=[0, 1, 2, 3, 4, 5], axis=0, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.drop(columns=[0, 2], axis=1, inplace=True)
    df.columns = ['2Theta', 'd', 'I/I1', 'FWHM', 'Integrated Int']
    df = df.astype(float, errors='raise')
    # discard low intensity data in DataFrame
    df = df[df['I/I1'] > 10]
    return df


def get_user_input(k=0.94, l=1.54056) -> tuple:
    """
    Get user input
    :param k - is Scherrer's  constant. K varies from 0.68 to 2.08. K = 0.94 for spherical crystallites with cubic symmetry
    :param l - is X-ray wavelength"""
    question = input('Do you want to use the default values of k=0.94 (for spherical crystallites with cubic symmetry) and λ=1.54056 Å? Enter y/n.')
    if question.lower() in ('n', 'no'):
        k = float(input("Enter K - Scherrer's  constant. K varies from 0.68 to 2.08. K = 0.94 for spherical crystallites with cubic symmetry"))
        l = float(input('Enter λ - X-ray wavelength.'))
    return k, l


def calc_size(df: pd.DataFrame, k: float, l: float) -> pd.DataFrame:
    """Calculate the particle_size based on data in dataframe"""
    radian = df['2Theta'] * np.pi / 360
    df['particle_size, nm'] =(k * l) / (df['FWHM'] * np.pi * 10 * np.cos(radian) /180)
    return df


def calc_mean_size(df: pd.DataFrame) -> float:
    """Calculate the mean size of the particles based on data in dataframe"""
    mean_size= df['particle_size, nm'].mean().round()
    return mean_size


def calc_error(df: pd.DataFrame, alpha=0.05) -> float:
    """Calculate the error of the particle size based on data in dataframe
    Alpha is significance level = 5% by default, n - the number of measurements i.e. points"""
    # Get the number of measurements i.e. points
    n = len(df['particle_size, nm'])
    # Calculate student t value
    v = t.ppf(1 - alpha/2, (n-1))
    # Calculate the error confidence interval
    error = df['particle_size, nm'].std() * v / np.sqrt(n)
    return error.round()


def main(file_name: str):
    """Main function"""
    df = read_table_from_pdf(file_name)
    df = clean_df(df)
    k, l = get_user_input()
    df = calc_size(df, k, l)
    mean_size, error = calc_mean_size(df), calc_error(df)
    print(f'The average crystallite size of the sample is {mean_size} nm, the error confidence interval is {error} nm')


if __name__ == '__main__':
    file_names = list(glob('*.pdf'))
    if not file_names:
        file_names = sys.argv[1:]
    for name in file_names:
        main(file_name=name)
