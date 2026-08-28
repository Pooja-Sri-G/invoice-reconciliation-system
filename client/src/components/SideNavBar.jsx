import React from 'react';

const SideNavBar = () => {
  const tabs = [
    { label: "Dashboard", icon: "dashboard", active: true },
    { label: "Invoices", icon: "receipt_long" },
    { label: "Discrepancies", icon: "rule" },
    { label: "Vendors", icon: "factory" },
    { label: "Settings", icon: "settings" },
  ];

  return (
    <aside className="h-screen w-64 fixed left-0 top-0 bg-surface-container-low border-r border-outline-variant flex flex-col py-6 px-4 shadow-sm">
      <div className="mb-8 px-2">
        <h2 className="text-xs font-bold uppercase tracking-wider text-on-surface-variant mb-4">System History</h2>
        <div className="flex items-center gap-3 p-3 bg-surface-container-lowest rounded-four border border-outline-variant">
          <div className="bg-primary/10 p-2 rounded">
            <span className="material-icons text-primary text-sm">history</span>
          </div>
          <div>
            <p className="text-xs font-bold">Recent Processing</p>
            <p className="text-[10px] text-on-surface-variant">Last job: 2m ago</p>
          </div>
        </div>
      </div>

      <nav className="flex-1 space-y-1">
        {tabs.map((tab) => (
          <div 
            key={tab.label}
            className={`flex items-center gap-3 px-4 py-3 cursor-pointer transition-all duration-200 ${
              tab.active 
                ? "bg-primary/10 text-primary font-bold rounded-lg" 
                : "text-on-surface-variant hover:bg-surface-container-high hover:text-primary rounded-lg"
            }`}
          >
            <span className="material-icons text-sm">{tab.icon}</span>
            <span className="text-sm">{tab.label}</span>
          </div>
        ))}
      </nav>

      <div className="mt-auto pt-6 border-t border-outline-variant space-y-1">
        <button className="w-full flex items-center gap-3 px-4 py-3 text-on-surface-variant hover:text-primary transition-colors">
          <span className="material-icons text-sm">help_outline</span>
          <span className="text-sm">Help Center</span>
        </button>
        <button className="w-full flex items-center gap-3 px-4 py-3 text-red-600 hover:bg-red-50 transition-colors rounded-lg">
          <span className="material-icons text-sm">logout</span>
          <span className="text-sm font-medium">Sign Out</span>
        </button>
      </div>
    </aside>
  );
};

export default SideNavBar;