import { useState } from 'react';
import './index.css';

function SecondPage({ onNavigateHome, onNavigateToDashboard }) {
  const [selectedTrees, setSelectedTrees] = useState({});
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCategory, setFilterCategory] = useState('all');

  // Tree species data with survival rates from the JSON
  const speciesData = {
    "Banyan": { survivalRate: 0.7 },
    "Gulmohar": { survivalRate: 0.8 },
    "Neem": { survivalRate: 0.85 },
    "Peepal": { survivalRate: 0.75 },
    "Mango": { survivalRate: 0.8 },
    "Teak": { survivalRate: 0.7 },
    "Jamun": { survivalRate: 0.75 },
    "Arjun": { survivalRate: 0.7 },
    "Sal": { survivalRate: 0.65 },
    "Sissoo": { survivalRate: 0.7 },
    "Kadam": { survivalRate: 0.75 },
    "Mahua": { survivalRate: 0.65 },
    "Yellow Bell": { survivalRate: 0.8 },
    "Casuarina": { survivalRate: 0.75 },
    "Coconut": { survivalRate: 0.85 },
    "Kadamba": { survivalRate: 0.7 },
    "Acacia": { survivalRate: 0.75 },
    "Indian Laburnum": { survivalRate: 0.8 },
    "Tamarind": { survivalRate: 0.75 },
    "Indian Gooseberry": { survivalRate: 0.8 },
    "Eucalyptus": { survivalRate: 0.65 },
    "Karanja": { survivalRate: 0.7 },
    "Jackfruit": { survivalRate: 0.7 },
    "Fig": { survivalRate: 0.75 },
    "Palmyra Palm": { survivalRate: 0.7 },
    "Silk Cotton": { survivalRate: 0.7 },
    "Indian Coral Tree": { survivalRate: 0.75 },
    "Bael": { survivalRate: 0.8 },
    "Flame of the Forest": { survivalRate: 0.7 },
    "Pongamia": { survivalRate: 0.7 },
    "Amla": { survivalRate: 0.8 },
    "Anjeer": { survivalRate: 0.75 },
    "Borassus": { survivalRate: 0.7 },
    "Semal": { survivalRate: 0.7 }
  };

  // Complete tree database with all 34 species
  const treeDatabase = {
    "Banyan": {
      category: 'Large Trees',
      description: 'Sacred tree with extensive canopy, excellent for large spaces',
      emoji: '🌳'
    },
    "Gulmohar": {
      category: 'Flowering Trees',
      description: 'Beautiful orange-red flowers, perfect for ornamental purposes',
      emoji: '🌺'
    },
    "Neem": {
      category: 'Medicinal Trees',
      description: 'Natural pesticide and medicinal properties, drought resistant',
      emoji: '🌿'
    },
    "Peepal": {
      category: 'Large Trees',
      description: 'Sacred fig tree, releases oxygen at night',
      emoji: '🍃'
    },
    "Mango": {
      category: 'Fruit Trees',
      description: 'King of fruits, provides delicious mangoes and shade',
      emoji: '🥭'
    },
    "Teak": {
      category: 'Timber Trees',
      description: 'Premium hardwood, excellent for furniture and construction',
      emoji: '🌲'
    },
    "Jamun": {
      category: 'Fruit Trees',
      description: 'Purple fruit with medicinal benefits, good for diabetics',
      emoji: '🫐'
    },
    "Arjun": {
      category: 'Medicinal Trees',
      description: 'Medicinal bark, good for heart health and riverbank plantation',
      emoji: '🌴'
    },
    "Sal": {
      category: 'Timber Trees',
      description: 'Sacred tree, valuable timber, good for construction',
      emoji: '🌱'
    },
    "Sissoo": {
      category: 'Timber Trees',
      description: 'Rosewood species, excellent for furniture and musical instruments',
      emoji: '🌾'
    },
    "Kadam": {
      category: 'Flowering Trees',
      description: 'Fragrant flowers, culturally significant, good shade tree',
      emoji: '🌸'
    },
    "Mahua": {
      category: 'Economic Trees',
      description: 'Flowers used for food and beverages, tribal economic importance',
      emoji: '🌼'
    },
    "Yellow Bell": {
      category: 'Flowering Trees',
      description: 'Bright yellow trumpet-shaped flowers, ornamental tree',
      emoji: '🔔'
    },
    "Casuarina": {
      category: 'Fast Growing',
      description: 'Wind-resistant, good for coastal areas and erosion control',
      emoji: '🌲'
    },
    "Coconut": {
      category: 'Palm Trees',
      description: 'Versatile palm providing coconuts, oil, and fiber',
      emoji: '🥥'
    },
    "Kadamba": {
      category: 'Large Trees',
      description: 'Round fragrant flowers, fast growing, good for landscaping',
      emoji: '🌻'
    },
    "Acacia": {
      category: 'Fast Growing',
      description: 'Drought tolerant, good for arid regions and soil improvement',
      emoji: '🌵'
    },
    "Indian Laburnum": {
      category: 'Flowering Trees',
      description: 'Golden yellow flowers, medicinal properties, ornamental',
      emoji: '🌕'
    },
    "Tamarind": {
      category: 'Fruit Trees',
      description: 'Tangy fruit, used in cooking, long-lived shade tree',
      emoji: '🍯'
    },
    "Indian Gooseberry": {
      category: 'Medicinal Trees',
      description: 'Rich in Vitamin C, high medicinal value, hardy tree',
      emoji: '🍈'
    },
    "Eucalyptus": {
      category: 'Fast Growing',
      description: 'Rapid growth, aromatic leaves, good for paper industry',
      emoji: '🌿'
    },
    "Karanja": {
      category: 'Economic Trees',
      description: 'Biodiesel production, coastal plantation, medicinal uses',
      emoji: '🌰'
    },
    "Jackfruit": {
      category: 'Fruit Trees',
      description: 'Large nutritious fruit, timber value, sustainable food source',
      emoji: '🍍'
    },
    "Fig": {
      category: 'Fruit Trees',
      description: 'Sweet figs, good for birds, religious significance',
      emoji: '🍇'
    },
    "Palmyra Palm": {
      category: 'Palm Trees',
      description: 'Traditional palm, sap used for jaggery, drought resistant',
      emoji: '🌴'
    },
    "Silk Cotton": {
      category: 'Large Trees',
      description: 'Cotton-like fibers, large buttressed trunk, deciduous',
      emoji: '☁️'
    },
    "Indian Coral Tree": {
      category: 'Flowering Trees',
      description: 'Bright red flowers, used for living fences, nitrogen fixing',
      emoji: '🪸'
    },
    "Bael": {
      category: 'Medicinal Trees',
      description: 'Sacred fruit, digestive properties, drought tolerant',
      emoji: '🍊'
    },
    "Flame of the Forest": {
      category: 'Flowering Trees',
      description: 'Spectacular orange-red flowers, state flower of several states',
      emoji: '🔥'
    },
    "Pongamia": {
      category: 'Economic Trees',
      description: 'Biodiesel tree, coastal areas, nitrogen fixing legume',
      emoji: '🌰'
    },
    "Amla": {
      category: 'Medicinal Trees',
      description: 'High Vitamin C content, Ayurvedic medicine, hardy tree',
      emoji: '🍈'
    },
    "Anjeer": {
      category: 'Fruit Trees',
      description: 'Nutritious figs, Mediterranean climate adaptation',
      emoji: '🍇'
    },
    "Borassus": {
      category: 'Palm Trees',
      description: 'Toddy palm, multiple economic uses, drought resistant',
      emoji: '🌴'
    },
    "Semal": {
      category: 'Large Trees',
      description: 'Silk cotton tree, large thorny trunk, kapok fiber production',
      emoji: '☁️'
    }
  };

  const categories = ['all', 'Large Trees', 'Flowering Trees', 'Medicinal Trees', 'Fruit Trees', 'Timber Trees', 'Palm Trees', 'Fast Growing', 'Economic Trees'];

  const filteredTrees = Object.entries(treeDatabase).filter(([name, data]) => {
    const matchesSearch = name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = filterCategory === 'all' || data.category === filterCategory;
    return matchesSearch && matchesCategory;
  });

  const updateTreeQuantity = (treeName, delta) => {
    setSelectedTrees(prev => {
      const currentQty = prev[treeName] || 0;
      const newQty = Math.max(0, currentQty + delta);
      if (newQty === 0) {
        const { [treeName]: removed, ...rest } = prev;
        return rest;
      }
      return { ...prev, [treeName]: newQty };
    });
  };

  const setTreeQuantity = (treeName, qty) => {
    if (qty <= 0) {
      const { [treeName]: removed, ...rest } = selectedTrees;
      setSelectedTrees(rest);
    } else {
      setSelectedTrees(prev => ({ ...prev, [treeName]: qty }));
    }
  };

  const calculateTotalImpact = () => {
    const totalSpecies = Object.keys(selectedTrees).length;
    const totalTrees = Object.values(selectedTrees).reduce((sum, qty) => sum + qty, 0);
    return { totalSpecies, totalTrees };
  };

  const impact = calculateTotalImpact();

  return (
    <div className="dashboard-container">
      {/* Left Panel - Selected Trees */}
      <div className="left-panel">
        {/* Header */}
        <div className="left-panel-header">
          <h2 className="left-panel-title">
            Selected Species ({impact.totalSpecies})
          </h2>
        </div>

        {/* Selected Trees List */}
        <div className="selected-trees-list">
          {Object.entries(selectedTrees).length === 0 ? (
            <div className="no-trees-message">
              <div className="no-trees-icon">🌱</div>
              <p>No trees selected yet. Choose trees from the right panel to get started.</p>
            </div>
          ) : (
            Object.entries(selectedTrees).map(([treeName, quantity]) => {
              const treeData = treeDatabase[treeName];
              
              return (
                <div key={treeName} className="selected-tree-item">
                  <div className="selected-tree-header">
                    <div className="selected-tree-info">
                      <div className="selected-tree-name">
                        <span>{treeData.emoji}</span>
                        {treeName}
                      </div>
                      <div className="selected-tree-quantity">
                        Quantity: {quantity} trees
                      </div>
                    </div>
                  </div>

                  {/* Quantity Controls */}
                  <div className="quantity-controls">
                    <button
                      onClick={() => updateTreeQuantity(treeName, -1)}
                      className="quantity-btn quantity-btn-minus"
                    >
                      -
                    </button>
                    
                    <input
                      type="number"
                      value={quantity}
                      onChange={(e) => setTreeQuantity(treeName, parseInt(e.target.value) || 0)}
                      className="quantity-input"
                    />
                    
                    <button
                      onClick={() => updateTreeQuantity(treeName, 1)}
                      className="quantity-btn quantity-btn-plus"
                    >
                      +
                    </button>
                  </div>

                  {/* Quick Add Buttons */}
                  <div className="quick-add-buttons">
                    {[10, 50, 100, 1000].map(amount => (
                      <button
                        key={amount}
                        onClick={() => updateTreeQuantity(treeName, amount)}
                        className="quick-add-btn"
                      >
                        +{amount}
                      </button>
                    ))}
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Generate Dashboard Button */}
        {Object.keys(selectedTrees).length > 0 && (
          <div className="generate-dashboard-section">
            <button
              onClick={() => {
                // Navigate to TreePlantingDashboard with selected trees data
                if (onNavigateToDashboard) {
                  onNavigateToDashboard(selectedTrees);
                } else {
                  // Fallback for testing
                  console.log('Navigate to dashboard with:', selectedTrees);
                  alert('Dashboard navigation - connect to your TreePlantingDashboard');
                }
              }}
              className="generate-dashboard-btn"
            >
              Generate Dashboard
            </button>
          </div>
        )}
      </div>

      {/* Right Panel - Tree Selection */}
      <div className="right-panel">
        {/* Header */}
        <div className="right-panel-header">
          <h1 className="main-title">
            Tree Species Selection Dashboard
          </h1>
          
          <div className="search-filters">
            {/* Search */}
            <div className="search-container">
              <span className="search-icon">
                🔍
              </span>
              <input
                type="text"
                placeholder="Search trees..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input"
              />
            </div>

            {/* Category Filter */}
            <select
              value={filterCategory}
              onChange={(e) => setFilterCategory(e.target.value)}
              className="category-select"
            >
              {categories.map(category => (
                <option key={category} value={category}>
                  {category === 'all' ? 'All Categories' : category}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Tree Cards */}
        <div className="tree-cards-container">
          <div className="tree-cards-grid">
            {filteredTrees.map(([treeName, treeData], index) => (
              <div
                key={treeName}
                className="tree-card"
                style={{
                  animationDelay: `${index * 0.05}s`
                }}
              >
                <div className="tree-card-header">
                  <div className="tree-card-info">
                    <div className="tree-name-container">
                      <span className="tree-emoji">{treeData.emoji}</span>
                      <h3 className="tree-name">
                        {treeName}
                      </h3>
                    </div>
                    <span className="tree-category-badge">
                      {treeData.category}
                    </span>
                  </div>
                </div>

                <p className="tree-description">
                  {treeData.description}
                </p>

                {/* Stats */}
                <div className="tree-stats">
                  <div className="tree-stat-item">
                    <div className="tree-stat-label">
                      Category
                    </div>
                    <div className="tree-stat-value tree-stat-category">
                      {treeData.category}
                    </div>
                  </div>
                  <div className="tree-stat-item">
                    <div className="tree-stat-label">
                      Survival Rate
                    </div>
                    <div className="tree-stat-value tree-stat-survival">
                      {speciesData[treeName] ? (speciesData[treeName].survivalRate * 100).toFixed(0) + '%' : 'N/A'}
                    </div>
                  </div>
                </div>

                {/* Add Button */}
                <button
                  onClick={() => updateTreeQuantity(treeName, 1)}
                  className="add-tree-btn"
                >
                  + Add Tree
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default SecondPage;