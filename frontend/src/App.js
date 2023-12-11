import { Routes, Route } from 'react-router-dom';

import Header from './components/Header/Header';
import Home from './pages/Home/Home';
import Settings from './pages/Settings/Settings';
import Drawer from './components/Sidebar/Drawer';

function App() {
  return (
    <>
      <Drawer />
      <Header />
      <Routes>
        <Route exact path='/' element={<Home />} />
        <Route path='/settings' element={<Settings />} />
        {/* <Route path='*' element={<NoPage />} /> */}
      </Routes>
    </>
  );
}

export default App;
