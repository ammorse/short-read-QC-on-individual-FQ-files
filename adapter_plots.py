#!/usr/bin/env python

##        DESCRIPTION: This program generates plots for assessing adapter content in a set of FASTQ files.
##        It takes a CSV of adapter content per sample and will output two plots: a bar chart showing the
##        percentage of reads with adapters by sample and a density plot that looks at the distribution of
##        adapter content across the set of FASTQ files.
##        
##        Author: Jeremy R. B. Newman


## Import packages
import argparse
import numpy as np
import scipy
from scipy.stats import gaussian_kde
import pandas
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


def getOptions():
    """ Function to pull in arguments """
    parser = argparse.ArgumentParser(description="Import CSV and give output names")
    parser.add_argument("--input", dest="csvInput", action='store', required=True, help="Input CSV")
    parser.add_argument("--obar", dest="outBar", action='store', required=True, help="Output filename of bar chart")
    parser.add_argument("--odensity", dest="outDensity", action='store', required=True, help="Output filename of density plot")
    parser.add_argument("--name", dest="setName", action='store', required=True, help='Name for the set of FASTQ files (e.g. "Plate 2")')

    args = parser.parse_args()
    return args

def main():
    # import data
    adapterContent=pandas.read_csv(args.csvInput, sep=',', header=None, skiprows=1)
    
    # Plot adapter content by sample
    xLabels=adapterContent[0]
    percAdapter=adapterContent[3]
    N=len(percAdapter)
    
    ind = np.arange(N)
    width = 0.1
    
    fig = plt.figure(figsize=(20,10))
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)
    
    width = .25
    ind = np.arange(N) 
    plt.bar(ind, percAdapter, width=width, color='k')
    plt.xticks(ind + width / 2, xLabels, rotation='vertical', size=6)
    barTitle='Adapter content by sample from ' + str(args.setName)
    ax.set_title(barTitle)
    
    ax.set_xlabel('SampleID')
    ax.set_ylabel('Adapter content (%)')
    
    fig.savefig(args.outBar)

    ### Plot overall distribution of adapter content
    fig1 = plt.figure(figsize=(10,10))
    
    # Data to plot
    percAdapterDist=adapterContent[3].tolist()
    
    num_bins = np.linspace(0,100,100)
    density = gaussian_kde(percAdapterDist)
    density.covariance_factor = lambda : .25
    density._compute_covariance()
    plt.plot(num_bins,density(num_bins))
    plt.xlabel('Percentage adapter content')
    densityTitle='Distribution of adapter content across ' + str(args.setName)
    plt.title(densityTitle)
    fig1.savefig(args.outDensity)

if __name__ == '__main__':
    # Parse command line arguments
    global args
    args = getOptions()
    main()

