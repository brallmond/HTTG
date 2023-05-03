#define test_cxx
#include "test.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>

void test::Loop()
{
//   In a ROOT session, you can do:
//      root> .L test.C
//      root> test t
//      root> t.GetEntry(12); // Fill t data members with entry number 12
//      root> t.Show();       // Show values of entry 12
//      root> t.Show(16);     // Read and show values of entry 16
//      root> t.Loop();       // Loop on all entries
//

//     This is the loop skeleton where:
//    jentry is the global entry number in the chain
//    ientry is the entry number in the current Tree
//  Note that the argument to GetEntry must be:
//    jentry for TChain::GetEntry
//    ientry for TTree::GetEntry and TBranch::GetEntry
//
//       To read only selected branches, Insert statements like:
// METHOD1:
//    fChain->SetBranchStatus("*",0);  // disable all branches
//    fChain->SetBranchStatus("branchname",1);  // activate branchname
// METHOD2: replace line
//    fChain->GetEntry(jentry);       //read all branches
//by  b_branchname->GetEntry(ientry); //read only this branch
   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();

   TFile* f = TFile::Open("../outputfiles/output_VBF_run3_cmsgrid_final.root", "recreate");
   TH1F* H_pt     = new TH1F("H_pt", "", 50, 0, 500);
   TH1F* H_eta    = new TH1F("H_eta", "", 50, -5, 5);
   TH1F* H_phi    = new TH1F("H_phi", "", 50, -6.3, 6.3);
   TH1F* H_energy = new TH1F("H_energy", "", 50, 0, 500);

   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      // if (Cut(ientry) < 0) continue;

      TLorentzVector Higgs;      
      for (int i = 0; i < Particle_; ++i) {
        // save Higgs
        if (Particle_PID[i] == 25) {
          Higgs.SetPtEtaPhiE(Particle_PT[i], Particle_Eta[i], \
                             Particle_Phi[i], Particle_E[i]);
        }
      }
      H_pt->Fill(    Higgs.Pt());
      H_eta->Fill(   Higgs.Eta());
      H_phi->Fill(   Higgs.Phi());
      H_energy->Fill(Higgs.E());

   } // end event loop
   H_pt->Write();
   H_eta->Write();
   H_phi->Write();
   H_energy->Write();

   f->Close();

}


















