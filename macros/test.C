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

   TFile* f = TFile::Open("../outputfiles/test_full_count.root", "recreate");
   TH1F* h_t1pt = new TH1F("h_t1pt", "", 100, 0, 200);
   TH1F* h_t2pt = new TH1F("h_t2pt", "", 100, 0, 200);
   TH1F* h_phpt = new TH1F("h_phpt", "", 100, 0, 200);

   int higgs_index = -2;
   int higgs_decay_count = 0;
   bool tau1_recorded = false;
   bool tau2_recorded = false;
   bool photon_recorded = false;

   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;

      TLorentzVector tau1;      
      TLorentzVector tau2;      
      TLorentzVector photon;      

      higgs_index = -2;
      tau1_recorded = false;
      tau2_recorded = false;
      photon_recorded = false;

      for (int i = 0; i < Particle_; ++i) {
        if (Particle_PID[i] == 25) {
          higgs_index = i;
        }

        // save taus
        if ((Particle_PID[i] == 15 || Particle_PID[i] == -15) && Particle_Mother2[i] == higgs_index) {
          // if no leading tau, save any tau as first tau
          if(tau1.Pt() == 0) {
            tau1.SetPtEtaPhiE(Particle_PT[i], Particle_Eta[i], \
                              Particle_Phi[i], Particle_E[i]);
            tau1_recorded = true;
          }
          // if no subleading tau, save as leading if new tau
          // has pT greater than first tau, otherwise
          // save as subleading tau
          else if (tau2.Pt() == 0) {
            if (Particle_PT[i] > tau1.Pt()) {
              tau2 = tau1;
              tau1.SetPtEtaPhiE(Particle_PT[i], Particle_Eta[i], \
                                Particle_Phi[i], Particle_E[i]);
            }
            else {
              tau2.SetPtEtaPhiE(Particle_PT[i], Particle_Eta[i], \
                                Particle_Phi[i], Particle_E[i]);
            }
            tau2_recorded = true;
          }
        }
        // save photon
        else if ((Particle_PID[i] == 22) && Particle_Mother2[i] == higgs_index) {
          photon.SetPtEtaPhiE(Particle_PT[i], Particle_Eta[i], \
                              Particle_Phi[i], Particle_E[i]);
          photon_recorded = true;
        }

        if (tau1_recorded && tau2_recorded && photon_recorded) {higgs_decay_count++;}

      }
      //std::cout << tau1.Pt() << '\t' << tau2.Pt() << '\t' << photon.Pt() << std::endl;
      h_t1pt->Fill(tau1.Pt());
      h_t2pt->Fill(tau2.Pt());
      h_phpt->Fill(photon.Pt());
   } // end event loop
   std::cout << "Higgs decay count: " << higgs_decay_count << std::endl;
   h_t1pt->Write();
   h_t2pt->Write();
   h_phpt->Write();

   f->Close();

}


















