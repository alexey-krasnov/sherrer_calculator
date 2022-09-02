#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import tabula


def read_table_from_pdf(pdf_name: str) -> pd.DataFrame:
    """Read a PDF File. Get DataFrame with data to process. It is the 1th table in list of parsed tables"""
    dfs = tabula.io.read_pdf(pdf_name, pages='1', pandas_options={'header': None})
    # print(len(dfs), *dfs, sep='\n\n')
    return dfs[0]


def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    # Clean data in DataFrame
    df.drop(labels=[0, 1, 2, 3, 4, 5], axis=0, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.drop(columns=[0, 2], axis=1, inplace=True)
    df.columns = ['2Theta', 'd', 'I/I1', 'FWHM', 'Integrated Int']
    df = df.astype(float, errors = 'raise')
    return df


def get_uset_input(k=0.94, l=1.54056) -> tuple:
    question = input('Do you want to use the default values of k=0.94 (for spherical crystallites with cubic symmetry) and λ=1.54056 Å? Enter y/n.')
    if question.lower() in ('n', 'no'):
        k = float(input('Enter K - Scherrer constant. K varies from 0.68 to 2.08. K = 0.94 for spherical crystallites with cubic symmetry'))
        l = float(input('Enter λ - X-ray wavelength.'))
    return k, l


def calc_size(df: pd.DataFrame, k: float, l:float) -> pd.DataFrame:
    radian = df['2Theta'] * np.pi / 360
    df['particle_size, nm'] =(k * l) / (df['FWHM'] * np.pi * 10 * np.cos(radian) /180)
    return df


def calc_mean_std_size(df: pd.DataFrame) -> tuple:
    df = df[df['I/I1'] > 10]
    mean_size, std = df['particle_size, nm'].mean().round(), df['particle_size, nm'].std().round()
    return mean_size, std


if __name__ == '__main__':
    df = read_table_from_pdf('Untitled.pdf')
    df = clean_df(df)
    k,l = get_uset_input()
    df = calc_size(df, k, l)
    mean_size, std = calc_mean_std_size(df)
    print(f'The average crystallite size of the sample is {mean_size}, the standard deviation is {std}')