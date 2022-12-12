import ROOT

def set_style(in_hist: ROOT.TH1F, line_color: int, marker_style: int, marker_color: int=1) -> None:
    """Set the style of a histogram (as a function since this is done often)"""
    """
    For colors,    1,   2,     3,    4 is
               black, red, green, blue
    For markers,   4,     25,       26 is
              circle, square, triangle
    """
    # set marker_color and line_color the same
    marker_color = line_color
    in_hist.SetLineColor(line_color)
    in_hist.SetMarkerStyle(marker_style)
    in_hist.SetMarkerColor(marker_color)


def set_labels(hist: ROOT.TH1F, hist_title: str, hist_yaxis: str, hist_xaxis: str) -> None:
    """Set the title and axis lables of a histogram"""
    hist.SetTitle(hist_title)
    hist.GetYaxis().SetTitle(hist_yaxis)
    hist.GetXaxis().SetTitle(hist_xaxis)

# name : [xaxis_max, ylog_boolean]
HTTG_AXIS_SETTINGS = {
    "h_t1pt" : [65, False],
    "h_t2pt" : [65, False],
    "h_phpt" : [70, True],
    }

