import { useState } from 'react';
import Firstpage from './Firstpage';
import Secondpage from './Secondpage';
import TreePlantingDashboard from './TreePlantingDashboard';
import './index.css';

function App() {
  const [currentPage, setCurrentPage] = useState('first');
  const [selectedTreesData, setSelectedTreesData] = useState({});

  const navigateToSecondPage = () => {
    setCurrentPage('second');
  };

  const navigateToFirstPage = () => {
    setCurrentPage('first');
  };

  const navigateToTreeDashboard = (treeData = null) => {
    if (treeData) {
      setSelectedTreesData(treeData);
    }
    setCurrentPage('dashboard');
  };

  return (
    <div className="App">
      {currentPage === 'first' && <Firstpage onGetStarted={navigateToSecondPage} />}
      {currentPage === 'second' && <Secondpage onNavigateHome={navigateToFirstPage} onNavigateToDashboard={navigateToTreeDashboard} />}
      {currentPage === 'dashboard' && <TreePlantingDashboard onNavigateHome={navigateToFirstPage} onNavigateToBasic={navigateToSecondPage} initialTreeData={selectedTreesData} />}
    </div>
  );
}

export default App;