import { BrowserRouter, Route, Routes } from "react-router-dom";
import MainPage from "./components/pages/MainPage";
import ChartsPage from "./components/pages/ChartsPage"
function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path='/' Component={MainPage}/>
          <Route path='/Charts' Component={ChartsPage}/>
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
