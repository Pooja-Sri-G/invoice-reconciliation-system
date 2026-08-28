import TopAppBar from '../components/TopAppBar';
import SideNavBar from '../components/SideNavBar';
import StatCard from '../components/StatCard';  
import React from 'react';

const ReconciliationResults = () => {
  return (
    <div className="min-h-screen bg-surface">
      <SideNavBar />
      <div className="pl-64">
        <TopAppBar />
        <main className="p-8 max-w-6xl mx-auto">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h1 className="text-3xl font-headline font-bold text-gray-900">Reconciliation Results</h1>
              <p className="text-on-surface-variant">Batch ID: #REC-2023-08-15</p>
            </div>
            <button className="flex items-center gap-2 bg-primary text-white px-6 py-3 rounded-four font-bold shadow-lg hover:brightness-110 active:scale-95 transition-all">
              <span className="material-icons text-sm">download</span>
              Download CSV Results
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <StatCard label="Total Invoices" value="48" icon="receipt" color="text-primary" />
            <StatCard label="Discrepancies" value="5" icon="warning" color="text-amber-500" />
            <StatCard label="Matched" value="43" icon="check_circle" color="text-green-600" />
          </div>

          <div className="bg-surface-container-lowest border border-outline-variant rounded-xl overflow-hidden shadow-sm">
            <table className="w-full text-left">
              <thead className="bg-surface-container-low border-b border-outline-variant">
                <tr>
                  <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider">Invoice ID</th>
                  <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider">Vendor</th>
                  <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider">Amount</th>
                  <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider">Status</th>
                  <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-outline-variant">
                {/* Map rows here */}
                <tr className="hover:bg-surface-container-low transition-colors">
                  <td className="px-6 py-4 text-sm font-medium">#INV-9921</td>
                  <td className="px-6 py-4 text-sm">Global Logistics Inc.</td>
                  <td className="px-6 py-4 text-sm font-bold">$12,450.00</td>
                  <td className="px-6 py-4">
                    <span className="bg-amber-100 text-amber-700 px-2 py-1 rounded text-[10px] font-bold uppercase">Discrepancy</span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button className="text-primary hover:underline text-sm font-bold">View Detail</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </main>
      </div>
    </div>
  );
};

const StatCard = ({ label, value, icon, color }) => (
  <div className="bg-surface-container-lowest p-6 border border-outline-variant rounded-xl shadow-sm">
    <div className="flex items-center justify-between mb-4">
      <span className={`material-icons ${color}`}>{icon}</span>
    </div>
    <p className="text-sm text-on-surface-variant font-medium">{label}</p>
    <p className="text-2xl font-bold">{value}</p>
  </div>
);

export default ReconciliationResults;