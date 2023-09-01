import { Routes, Route } from 'react-router-dom';

import Home from './pages/Home/Home';
import Settings from './pages/Settings/Settings';

function App() {
  return (
    <Routes>
      <Route exact path='/' element={<Home />} />
      <Route path='/settings' element={<Settings />} />
      {/* <Route path='*' element={<NoPage />} /> */}
    </Routes>
  );
}

export default App;
