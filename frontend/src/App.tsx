import { BrowserRouter, Route, Routes } from "react-router-dom";
import MainPage from "./components/pages/MainPage";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path='/' Component={MainPage}/>
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
