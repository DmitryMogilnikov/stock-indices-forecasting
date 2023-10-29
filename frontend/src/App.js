import React from 'react';
import Header from "./components/Header"
import Main_DataFillingForm from './components/Main_DataFillingForm';
import Main_DataTable from './components/Main_DataTable';

function App() {
  return (
    <div className="App">
      <Header />
      <Main_DataFillingForm />
      <Main_DataTable />
    </div>
  );
}

export default App;
