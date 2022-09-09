#!/usr/bin/env python
# coding: utf-8

"""Automatic XRD crystallite (grain) size calculator (Scherrer Equation)"""

from glob import glob
import sys
import numpy as np
import pandas as pd
from scipy.stats import t
import tabula


def read_table_from_pdf(pdf_name: str) -> pd.DataFrame:
    """Read a PDF File. Get DataFrame with XRD data to process.
    It is the 1st table in the list of parsed tables"""
    dfs = tabula.io.read_pdf(pdf_name, pages='1', pandas_options={'header': None})
    xrd_data = dfs[0]
    return xrd_data


def read_sample_name_from_pdf(pdf_name: str) -> tuple[str]:
    """Read a PDF File to get the sample data and sample name."""
    dfs = tabula.io.read_pdf(pdf_name, pages='2', lattice=True, pandas_options={'header': None})
    sample_data = dfs[1].at[2, 0].split(':')[1].strip()
    sample_name = dfs[1].at[3, 0].split(':')[1].strip()
    return sample_data, sample_name


def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    """Clean data in DataFrame.
    Represent useful data of XRD measurement as '2Theta', 'd', 'I/I1', 'FWHM', 'Integrated Int'."""
    df.drop(labels=[0, 1, 2, 3, 4, 5], axis=0, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.drop(columns=[0, 2], axis=1, inplace=True)
    df.columns = ['2Theta', 'd', 'I/I1', 'FWHM', 'Integrated Int']
    df = df.astype(float)
    # discard low intensity data in DataFrame
    df = df[df['I/I1'] > 10]
    return df


def get_user_input(k=0.94, l=1.54056) -> tuple:
    """Get user input
    :param k - is Scherrer's  constant.
    k varies from 0.68 to 2.08. k = 0.94 for spherical crystallites with cubic symmetry
    :param l - is X-ray wavelength"""
    question = input('Do you want to use the default values of k=0.94 '
                     '(for spherical crystallites with cubic symmetry) and λ=1.54056 Å? Enter y/n.')
    if question.lower() in ('n', 'no'):
        try:
            k = float(input("Enter K - Scherrer's  constant. K varies from 0.68 to 2.08. "
                            "K = 0.94 for spherical crystallites with cubic symmetry"))
            l = float(input('Enter λ - X-ray wavelength.'))
        except ValueError:
            print("Please enter the values with dot only e.g. 0.94 or 1.54056.")
    if question.lower() not in ('yes', 'no', 'y', 'n'):
        print('Please enter y/n.')
    print(f'The program is using the following values: k={k} and λ={l} Å,')
    return k, l


def calc_size(df: pd.DataFrame, k: float, l: float) -> pd.DataFrame:
    """Calculate the particle_size based on the data in dataframe"""
    radian = df['2Theta'] * np.pi / 360
    df['particle_size, nm'] = (k * l) / (df['FWHM'] * np.pi * 10 * np.cos(radian) / 180)
    return df


def calc_mean_size(df: pd.DataFrame) -> float:
    """Calculate the mean size of the particles based on the data in dataframe"""
    mean_size = df['particle_size, nm'].mean().round()
    return mean_size


def calc_error(df: pd.DataFrame, alpha=0.05) -> float:
    """Calculate the measurement error of the particle size based on data in dataframe
    Alpha is significance level = 5% by default, n - the number of measurements i.e. points"""
    # Get the number of measurements i.e. points
    n = len(df['particle_size, nm'])
    # Calculate student t value
    v = t.ppf(1 - alpha/2, (n-1))
    # Calculate the error confidence interval
    error = df['particle_size, nm'].std() * v / np.sqrt(n)
    return error.round()


def write_data_in_file(sample_name, sample_data, mean_size, error):
    """Export data in csv file"""
    dict_ = {'sample_name': [sample_name],
             'sample_data': [sample_data],
             'mean_size, nm': [mean_size],
             'error, nm': [error],
             }
    df = pd.DataFrame(dict_)
    if glob('sherrer_size_data.csv'):
        mode = 'a'
        header = False
    else:
        mode = 'w'
        header = list(dict_.keys())
    with open('sherrer_size_data.csv', mode=mode, encoding='utf-8') as f:
        df.to_csv(f, header=header, index=False)


def main(file_name: str):
    """Main function"""
    df = read_table_from_pdf(file_name)
    sample_data, sample_name = read_sample_name_from_pdf(file_name)
    df = clean_df(df)
    print(f'Data after cleaning: \n{df}')
    k, l = get_user_input()
    df = calc_size(df, k, l)
    mean_size, error = calc_mean_size(df), calc_error(df)
    print(f'The average crystallite size of the sample is {mean_size} nm, '
          f'the error confidence interval is {error} nm\n')
    write_data_in_file(sample_name, sample_data, mean_size, error)


if __name__ == '__main__':
    file_names = list(glob('*.pdf'))
    if not file_names:
        file_names = sys.argv[1:]
    for name in file_names:
        main(file_name=name)
