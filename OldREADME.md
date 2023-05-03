#MadGraph Plotting

This is a small repo to plot LHE files produced by MadGraph.

Currently working in C with the following workflow:
root -l
root [0] .L BlankTest.C
root [1] BlankTest t("input_file.root")
root [2] t.Loop("output_file.root")
root [3] .q
root -l output_file.root
root [0] h_t1pt->Draw()
and other available branch names.

Planning to switch to pyroot in the near future.
