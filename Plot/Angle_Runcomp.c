#include <TFile.h>
#include <TH1D.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <iostream>

int Angle_Runcomp() {
    // File names
    const char* file1_name = "ncgammaNTag_SK5_BERT.mc.root";
    const char* file2_name = "ncgammaNTagSKG4_BERTt2k_new.mc.root";

    // Histogram name
    const char* hist_name = "hangle_ncgamma_angle_all";

    // Open the files
    TFile* file1 = TFile::Open(file1_name, "READ");
    if (!file1 || file1->IsZombie()) {
        std::cerr << "Error: Cannot open file " << file1_name << std::endl;
        return 1;
    }

    TFile* file2 = TFile::Open(file2_name, "READ");
    if (!file2 || file2->IsZombie()) {
        std::cerr << "Error: Cannot open file " << file2_name << std::endl;
        return 1;
    }

    // Retrieve histograms
    TH1D* hist1 = dynamic_cast<TH1D*>(file1->Get(hist_name));
    if (!hist1) {
        std::cerr << "Error: Cannot find histogram " << hist_name << " in file " << file1_name << std::endl;
        return 1;
    }

    TH1D* hist2 = dynamic_cast<TH1D*>(file2->Get(hist_name));
    if (!hist2) {
        std::cerr << "Error: Cannot find histogram " << hist_name << " in file " << file2_name << std::endl;
        return 1;
    }

    // Create a canvas
    TCanvas* canvas = new TCanvas("canvas", "Histogram Comparison", 600, 600);

    // Draw histograms
    hist1->Scale(1.0/hist1->Integral());
    hist1->SetLineColor(kRed); // Set color for first histogram
    hist1->SetLineWidth(2);    // Set line width for first histogram
    hist1->SetStats(0);
    hist1->Draw("HIST");       // Draw the first histogram

    hist2->Scale(1.0/hist2->Integral());
    hist2->SetLineColor(kRed); // Set color for second histogram
    hist2->SetLineStyle(2);
    hist2->SetLineWidth(2); 
    hist2->SetStats(0);    // Set line width for second histogram
    hist2->Draw("HIST SAME");   // Draw the second histogram on the same canvas

    // Add a legend
    TLegend* legend = new TLegend(0.3, 0.7, 0.69, 0.89);
    legend->AddEntry(hist1, "Run10 - BERT", "l");
    legend->AddEntry(hist2, "Run11 - BERT", "l");
    legend->Draw();

    // Update and save the canvas
    //canvas->Update();
    //canvas->SaveAs("histogram_comparison.png");

    // Clean up
    //file1->Close();
    //file2->Close();
    //delete file1;
    //delete file2;

    //return 0;
}

