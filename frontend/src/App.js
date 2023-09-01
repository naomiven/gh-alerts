import { BrowserRouter, Routes, Route } from 'react-router-dom';

import Settings from './pages/Settings/Settings';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Settings />}>
          <Route index element={<Settings />} />
          <Route path='settings' element={<Settings />} />
          {/* <Route path='*' element={<NoPage />} /> */}
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
