import React, { useState, useEffect } from 'react';
import { Plus, Minus, Download, Search, TreePine, Apple, Palmtree, Sprout } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts';

// Custom tree icons using emojis
const TreeIcon = ({ emoji, size = 20 }) => (
  <span style={{ fontSize: size, lineHeight: 1 }}>{emoji}</span>
);

const TreeSpeciesDashboard = () => {
  const [selectedSpecies, setSelectedSpecies] = useState([
    { id: 1, name: 'Banyan', quantity: 6, category: 'Large Trees', description: 'Hardy tree with extensive root system', survivalRate: 85, emoji: '🌳', color: '#1f77b4' },
    { id: 2, name: 'Gulmohar', quantity: 7, category: 'Medicinal Trees', description: 'Ornamental flowering tree with medicinal properties', survivalRate: 78, emoji: '🌸', color: '#ff7f0e' },
    { id: 3, name: 'Neem', quantity: 3, category: 'Medicinal Trees', description: 'Natural pesticide, Ayurvedic medicine', survivalRate: 92, emoji: '🌿', color: '#2ca02c' }
  ]);

  const [currentView, setCurrentView] = useState('cumulative');

  // Sample data for the charts (simulating the matplotlib calculations)
  const generateChartData = () => {
    const years = Array.from({ length: 20 }, (_, i) => i + 1);
    
    return years.map(year => {
      const dataPoint = { year };
      
      selectedSpecies.forEach(species => {
        // Simulate CO₂ sequestration calculation
        const maxBiomass = 150 * species.quantity; // kg per tree * quantity
        const k = 0.3;
        const growth = maxBiomass / (1 + Math.exp(-k * (year - 10)));
        const co2Rate = growth * 0.5 * 3.67 * (species.survivalRate / 100); // Simplified calculation
        
        if (currentView === 'cumulative') {
          // Cumulative calculation
          dataPoint[species.name] = Math.round(co2Rate * year * 0.8);
        } else {
          // Annual rate
          dataPoint[species.name] = Math.round(co2Rate);
        }
      });
      
      return dataPoint;
    });
  };

  const generateBarData = () => {
    return selectedSpecies.map(species => {
      const totalCO2 = Math.round(species.quantity * 150 * 20 * 0.5 * 3.67 * (species.survivalRate / 100));
      return {
        name: species.name,
        total: totalCO2,
        fill: species.color
      };
    });
  };

  const chartData = generateChartData();
  const barData = generateBarData();

  const updateQuantity = (id, change) => {
    setSelectedSpecies(prev => prev.map(species => {
      if (species.id === id) {
        const newQuantity = Math.max(0, species.quantity + change);
        return { ...species, quantity: newQuantity };
      }
      return species;
    }).filter(species => species.quantity > 0));
  };

  const exportToPDF = () => {
    const printContent = `
      <div style="font-family: Arial, sans-serif; padding: 20px; color: #1e293b;">
        <h1 style="color: #4ade80; margin-bottom: 30px;">CO₂ Sequestration Analysis Report</h1>
        <div style="margin-bottom: 30px;">
          <h2 style="color: #334155; border-bottom: 2px solid #4ade80; padding-bottom: 10px;">Selected Species Analysis</h2>
          ${selectedSpecies.map(species => `
            <div style="margin: 20px 0; padding: 15px; border: 1px solid #e2e8f0; border-radius: 8px;">
              <h3 style="color: ${species.color}; margin: 0 0 10px 0;">${species.name}</h3>
              <p style="margin: 5px 0; color: #64748b;"><strong>Quantity:</strong> ${species.quantity} trees</p>
              <p style="margin: 5px 0; color: #64748b;"><strong>Survival Rate:</strong> ${species.survivalRate}%</p>
              <p style="margin: 5px 0; color: #64748b;"><strong>Est. Total CO₂ Captured:</strong> ${Math.round(species.quantity * 150 * 20 * 0.5 * 3.67 * (species.survivalRate / 100))} kg over 20 years</p>
            </div>
          `).join('')}
        </div>
        <div style="margin-top: 30px;">
          <h3 style="color: #334155;">Total Trees: ${selectedSpecies.reduce((sum, species) => sum + species.quantity, 0)}</h3>
          <h3 style="color: #334155;">Total CO₂ Sequestration: ${barData.reduce((sum, item) => sum + item.total, 0)} kg over 20 years</h3>
          <p style="color: #64748b; margin-top: 10px;">Generated on: ${new Date().toLocaleDateString()}</p>
        </div>
      </div>
    `;

    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
      <html>
        <head>
          <title>CO₂ Sequestration Report</title>
          <style>
            @media print {
              body { margin: 0; }
            }
          </style>
        </head>
        <body>
          ${printContent}
        </body>
      </html>
    `);
    printWindow.document.close();
    printWindow.print();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      <div className="flex">
        {/* Left Sidebar */}
        <div className="w-80 bg-slate-800/50 backdrop-blur-sm border-r border-slate-700 min-h-screen p-6">
          <div className="mb-8">
            <h2 className="text-lg font-semibold text-green-400 mb-4">Selected Species ({selectedSpecies.length})</h2>
            
            {selectedSpecies.map((species) => {
              const IconComponent = species.icon;
              return (
                <div key={species.id} className="mb-6 p-4 bg-slate-700/30 rounded-lg border border-slate-600">
                  <div className="flex items-center gap-3 mb-3">
                    <TreeIcon emoji={species.emoji} size={20} />
                    <h3 className="font-medium text-white">{species.name}</h3>
                  </div>
                  <p className="text-sm text-slate-400 mb-3">Quantity: {species.quantity} trees</p>
                  
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => updateQuantity(species.id, -1)}
                        className="w-8 h-8 bg-red-500 hover:bg-red-600 rounded flex items-center justify-center transition-colors"
                      >
                        <Minus size={14} />
                      </button>
                      <span className="w-12 text-center font-mono bg-slate-600 py-1 rounded">
                        {species.quantity}
                      </span>
                      <button
                        onClick={() => updateQuantity(species.id, 1)}
                        className="w-8 h-8 bg-green-500 hover:bg-green-600 rounded flex items-center justify-center transition-colors"
                      >
                        <Plus size={14} />
                      </button>
                    </div>
                  </div>
                  
                  <div className="flex gap-2 mb-2">
                    <button
                      onClick={() => updateQuantity(species.id, 10)}
                      className="px-2 py-1 bg-slate-600 hover:bg-slate-500 rounded text-xs transition-colors"
                    >
                      +10
                    </button>
                    <button
                      onClick={() => updateQuantity(species.id, 50)}
                      className="px-2 py-1 bg-slate-600 hover:bg-slate-500 rounded text-xs transition-colors"
                    >
                      +50
                    </button>
                    <button
                      onClick={() => updateQuantity(species.id, 100)}
                      className="px-2 py-1 bg-slate-600 hover:bg-slate-500 rounded text-xs transition-colors"
                    >
                      +100
                    </button>
                    <button
                      onClick={() => updateQuantity(species.id, 1000)}
                      className="px-2 py-1 bg-slate-600 hover:bg-slate-500 rounded text-xs transition-colors"
                    >
                      +1000
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
          
          <button
            onClick={exportToPDF}
            className="w-full bg-green-500 hover:bg-green-600 text-white py-3 px-4 rounded-lg flex items-center justify-center gap-2 font-medium transition-colors mb-4"
          >
            <Download size={20} />
            GENERATE DASHBOARD
          </button>
        </div>

        {/* Main Content - Charts */}
        <div className="flex-1 p-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-green-400 text-center mb-8">
              CO₂ Sequestration Analysis Dashboard
            </h1>
            
            <div className="flex gap-4 mb-6 justify-center">
              <button
                onClick={() => setCurrentView('cumulative')}
                className={`px-6 py-2 rounded-lg font-medium transition-colors ${
                  currentView === 'cumulative' 
                    ? 'bg-green-500 text-white' 
                    : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                }`}
              >
                Cumulative CO₂
              </button>
              <button
                onClick={() => setCurrentView('annual')}
                className={`px-6 py-2 rounded-lg font-medium transition-colors ${
                  currentView === 'annual' 
                    ? 'bg-green-500 text-white' 
                    : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                }`}
              >
                Annual Rate
              </button>
            </div>
          </div>

          {selectedSpecies.length > 0 ? (
            <div className="space-y-8">
              {/* Line Chart */}
              <div className="bg-slate-700/20 backdrop-blur-sm border border-slate-600 rounded-xl p-6">
                <h2 className="text-xl font-semibold text-white mb-4">
                  {currentView === 'cumulative' 
                    ? 'Cumulative CO₂ Sequestration Over 20 Years' 
                    : 'Annual CO₂ Sequestration Rate'}
                </h2>
                <ResponsiveContainer width="100%" height={400}>
                  <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
                    <XAxis 
                      dataKey="year" 
                      stroke="#94a3b8"
                      tick={{ fill: '#94a3b8' }}
                    />
                    <YAxis 
                      stroke="#94a3b8"
                      tick={{ fill: '#94a3b8' }}
                      label={{ value: 'CO₂ Captured (kg)', angle: -90, position: 'insideLeft', style: { textAnchor: 'middle', fill: '#94a3b8' } }}
                    />
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: '#1e293b', 
                        border: '1px solid #475569',
                        borderRadius: '8px',
                        color: '#fff'
                      }}
                    />
                    <Legend />
                    {selectedSpecies.map((species) => (
                      <Line 
                        key={species.name}
                        type="monotone" 
                        dataKey={species.name} 
                        stroke={species.color}
                        strokeWidth={2}
                        dot={{ fill: species.color, strokeWidth: 2, r: 4 }}
                      />
                    ))}
                  </LineChart>
                </ResponsiveContainer>
              </div>

              {/* Bar Chart */}
              <div className="bg-slate-700/20 backdrop-blur-sm border border-slate-600 rounded-xl p-6">
                <h2 className="text-xl font-semibold text-white mb-4">
                  Total CO₂ Captured by Each Species (20 Years)
                </h2>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={barData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
                    <XAxis 
                      dataKey="name" 
                      stroke="#94a3b8"
                      tick={{ fill: '#94a3b8' }}
                      angle={-45}
                      textAnchor="end"
                      height={80}
                    />
                    <YAxis 
                      stroke="#94a3b8"
                      tick={{ fill: '#94a3b8' }}
                      label={{ value: 'CO₂ Captured (kg)', angle: -90, position: 'insideLeft', style: { textAnchor: 'middle', fill: '#94a3b8' } }}
                    />
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: '#1e293b', 
                        border: '1px solid #475569',
                        borderRadius: '8px',
                        color: '#fff'
                      }}
                    />
                    <Bar dataKey="total" />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              {/* Summary Stats */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-slate-700/20 backdrop-blur-sm border border-slate-600 rounded-xl p-6 text-center">
                  <h3 className="text-lg font-semibold text-green-400 mb-2">Total Trees</h3>
                  <p className="text-3xl font-bold text-white">
                    {selectedSpecies.reduce((sum, species) => sum + species.quantity, 0)}
                  </p>
                </div>
                <div className="bg-slate-700/20 backdrop-blur-sm border border-slate-600 rounded-xl p-6 text-center">
                  <h3 className="text-lg font-semibold text-green-400 mb-2">Total CO₂ (20 years)</h3>
                  <p className="text-3xl font-bold text-white">
                    {barData.reduce((sum, item) => sum + item.total, 0).toLocaleString()} kg
                  </p>
                </div>
                <div className="bg-slate-700/20 backdrop-blur-sm border border-slate-600 rounded-xl p-6 text-center">
                  <h3 className="text-lg font-semibold text-green-400 mb-2">Avg Survival Rate</h3>
                  <p className="text-3xl font-bold text-white">
                    {Math.round(selectedSpecies.reduce((sum, species) => sum + species.survivalRate, 0) / selectedSpecies.length)}%
                  </p>
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center py-16">
              <div className="text-slate-400 text-lg">No species selected</div>
              <p className="text-slate-500 mt-2">Please select species from the sidebar to view CO₂ sequestration analysis</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TreeSpeciesDashboard;