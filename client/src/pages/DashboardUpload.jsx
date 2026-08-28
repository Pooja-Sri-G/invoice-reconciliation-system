import TopAppBar from '../components/TopAppBar';
import SideNavBar from '../components/SideNavBar';
import React from 'react';


const DashboardUpload = () => {
  return (
    <div className="min-h-screen bg-surface">
      <SideNavBar />
      <div className="pl-64">
        <TopAppBar />
        <main className="p-8 max-w-5xl mx-auto">
          <header className="mb-8">
            <h1 className="text-3xl font-headline font-bold text-gray-900">Upload Invoices</h1>
            <p className="text-on-surface-variant">Drag and drop your PDF invoices to start the reconciliation process.</p>
          </header>

          <div className="bg-surface-container-lowest border-2 border-dashed border-outline-variant rounded-xl p-12 flex flex-col items-center justify-center text-center cursor-pointer hover:border-primary transition-colors">
            <div className="w-16 h-16 bg-primary/5 rounded-full flex items-center justify-center mb-4">
              <span className="material-icons text-primary text-3xl">upload_file</span>
            </div>
            <h3 className="text-lg font-bold mb-1">Click or drag files here</h3>
            <p className="text-sm text-on-surface-variant mb-6">Supports multiple PDF files up to 50MB total.</p>
            <button className="bg-primary text-white px-8 py-3 rounded-four font-bold shadow-md hover:brightness-110 active:scale-95 transition-all">
              Select Files
            </button>
          </div>

          <section className="mt-12">
            <h2 className="text-xl font-bold mb-4">Processing History</h2>
            {/* Table or list component for recent jobs */}
          </section>
        </main>
      </div>
    </div>
  );
};

export default DashboardUpload;