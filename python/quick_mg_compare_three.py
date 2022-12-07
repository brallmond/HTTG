import ROOT
import os
import sys
#import re
#import array

from style_functions import set_style, set_labels
#ROOT.gROOT.SetBatch(True) # sets visual display off (i.e. no graphs/TCanvas)

def make_comparison_plot(in_file_one: 'str', in_file_two: 'str', in_file_three: 'str',
    var: 'str', label_one: 'str', label_two: 'str', label_three: 'str') -> 'None':
    """Create and save comparison of loose/tight efficiency plot"""

    # make two drawing pads on one canvas
    can = ROOT.TCanvas("can", "", 800, 600)

    ROOT.gStyle.SetOptStat(0)
    ROOT.TH1.SetDefaultSumw2()

    hist_var = var

    root_file_one = ROOT.TFile.Open(in_file_one, "READ") 
    h_one = root_file_one.Get(hist_var)
    h_one.SetDirectory(0) # keeps open after file close
    root_file_one.Close()

    root_file_two = ROOT.TFile.Open(in_file_two, "READ")
    h_two = root_file_two.Get(hist_var)
    h_two.SetDirectory(0)
    root_file_two.Close()

    root_file_three = ROOT.TFile.Open(in_file_three, "READ")
    h_three = root_file_three.Get(hist_var)
    h_three.SetDirectory(0)
    root_file_three.Close()

    # set styles and labels
    set_style(h_one, 4, 4)
    #ROOT.gPad.SetLogx()
    set_labels(h_one, var, "Events", var)
    h_one.Draw("HIST, PE")

    set_style(h_two, 2, 25)
    h_two.Draw("SAME, PE")

    set_style(h_three, 1, 26)
    h_three.Draw("SAME, PE")

    leg = ROOT.TLegend(0.55, 0.67, 0.9, 0.9)
    leg.SetTextSize(0.025)
    leg.AddEntry(h_one, label_one)
    leg.AddEntry(h_two, label_two)
    leg.AddEntry(h_three, label_three)
    leg.Draw()

    can.SaveAs("compare_"+var+".png")
    #input() # preserve graph display until user input


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--in_file_one', '-i1', required=True, action='store', help='input file one')
    parser.add_argument('--in_file_two', '-i2', required=True, action='store', help='input file two')
    parser.add_argument('--in_file_three', '-i3', required=True, action='store', help='input file three')

    args = parser.parse_args()

    label_one = "GC_15_100x"
    label_two = "GC_15_10x"
    label_three = "GC_15_1x"

    variables = ["h_t1pt", "h_t2pt", "h_phpt"]

    for var in variables:
      make_comparison_plot(args.in_file_one, args.in_file_two, args.in_file_three, var, \
                           label_one, label_two, label_three)

