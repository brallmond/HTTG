import ROOT
import shutil
import os
import sys

from style_functions import set_style, set_labels, HTTG_AXIS_SETTINGS
#ROOT.gROOT.SetBatch(True) # sets visual display off (i.e. no graphs/TCanvas)

def make_comparison_plot(in_file_one: 'str', in_file_two: 'str',
    var: 'str', label_one: 'str', label_two: 'str') -> 'None':
    """Create and save comparison of loose/tight efficiency plot"""

    # make two drawing pads on one canvas
    can = ROOT.TCanvas("can", "", 800, 600)

    ROOT.gStyle.SetOptStat(0)
    ROOT.TH1.SetDefaultSumw2()

    #hist_var = var

    root_file_one = ROOT.TFile.Open(in_file_one, "READ") 
    #h_one = root_file_one.Get(hist_var)
    h_one = root_file_one.Get(var)
    h_one.SetDirectory(0) # keeps open after file close
    root_file_one.Close()

    root_file_two = ROOT.TFile.Open(in_file_two, "READ")
    h_two = root_file_two.Get(var)
    h_two.SetDirectory(0)
    root_file_two.Close()

    # set xaxis maximum and ylog True/False
    xaxis_min = HTTG_AXIS_SETTINGS[var][0]
    xaxis_max = HTTG_AXIS_SETTINGS[var][1]
    ylog_boolean = HTTG_AXIS_SETTINGS[var][2]

    # set styles and labels
    set_style(h_one, 4, 4)
    set_labels(h_one, var, "Events", var)
    h_one.GetXaxis().SetRangeUser(xaxis_min, xaxis_max)
    if (ylog_boolean):
      ROOT.gPad.SetLogy()
    h_one.Draw("HIST, PE")

    set_style(h_two, 1, 26)
    h_two.Draw("SAME, PE")

    leg = ROOT.TLegend(0.35, 0.77, 0.55, 0.9)
    leg.SetTextSize(0.025)
    leg.AddEntry(h_one, label_one)
    leg.AddEntry(h_two, label_two)
    leg.Draw()

    can.SaveAs("compare_"+var+".png")
    #input() # preserve graph display until user input


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--in_file_one', '-i1', required=True, action='store', help='input file one')
    parser.add_argument('--in_file_two', '-i2', required=True, action='store', help='input file two')
    parser.add_argument('--label_one', '-l1', required=True, action='store', help='label one')
    parser.add_argument('--label_two', '-l2', required=True, action='store', help='label two')

    args = parser.parse_args()

    #variables = ["h_t1pt", "h_t2pt", "h_phpt"]
    #variables = ["H_pt", "H_eta", "H_phi", "H_energy"]
    variables = [
                 "H_pt", "H_eta", "H_phi", "H_energy",
                 "J1_pt", "J1_eta", "J1_phi", "J1_energy",
                 "J2_pt", "J2_eta", "J2_phi", "J2_energy",
                 "J3_pt", "J3_eta", "J3_phi", "J3_energy",
                 "mjj", "pair_deta",
                ]

    for var in variables:
      make_comparison_plot(args.in_file_one, args.in_file_two, var, \
                           args.label_one, args.label_two)

    source_dir = '/Users/ballmond/HTTG/python'
    target_dir = '/Users/ballmond/HTTG/graphs'
        
    file_names = os.listdir(source_dir)
    file_names = [file_name for file_name in file_names if ".png" in file_name]
        
    for file_name in file_names:

      if os.path.isfile(target_dir + '/' + file_name):  
        os.remove(target_dir + '/' + file_name)

      shutil.move(os.path.join(source_dir, file_name), target_dir)



