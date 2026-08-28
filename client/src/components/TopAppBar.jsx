import React from 'react';

const TopAppBar = () => {
  return (
    <header className="bg-surface-container-lowest border-b border-outline-variant w-full h-16 sticky top-0 z-50 flex items-center justify-between px-6 mx-auto">
      <div className="flex items-center gap-4">
        <span className="text-2xl font-bold text-primary font-headline">FinReconcile</span>
        <div className="relative ml-8">
           {/* Search Bar implementation */}
           <input 
             type="text" 
             placeholder="Search invoices..." 
             className="bg-surface-container-low px-4 py-2 rounded-four text-sm w-64 border-none focus:ring-2 focus:ring-primary"
           />
        </div>
      </div>
      
      <div className="flex items-center gap-4">
        <button className="p-2 hover:bg-surface-container-high rounded-full transition-colors">
          <span className="material-icons text-on-surface-variant">notifications</span>
        </button>
        <button className="p-2 hover:bg-surface-container-high rounded-full transition-colors">
          <span className="material-icons text-on-surface-variant">help</span>
        </button>
        <div className="flex items-center gap-2 ml-2 cursor-pointer">
          <img 
            src="/api/placeholder/32/32" 
            alt="User profile avatar" 
            className="w-8 h-8 rounded-full border border-outline-variant"
          />
          <span className="text-sm font-medium">Alex Rivera</span>
        </div>
      </div>
    </header>
  );
};

export default TopAppBar;