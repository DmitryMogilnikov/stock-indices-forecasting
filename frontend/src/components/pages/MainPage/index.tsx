import React from "react";
import Header from "./header/Header";
import MainDataFillingForm from "./FillingForm/container";
import MainDataTable from "./DataTable/container";

const MainPage = () => {
    return(
        <div id="mainPage">
            <Header />
            <MainDataFillingForm />
            <MainDataTable />
        </div>
    )
}

export default MainPage