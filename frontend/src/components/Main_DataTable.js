import React from "react";
import "./../styles/Main_DataTable.model.scss";

function Main_DataTable() {
    return (
        <div className="Main_DataTable">
            <table id="dataTable" name="dataTable" className="dataTable">
                <tr>
                    <th>Дата</th>
                    <th>Цена</th>
                    <th>Откр.</th>
                    <th>Макс.</th>
                    <th>Мин.</th>
                    <th>Интегральная<br></br>сумма</th>
                    <th>Процентный<br></br>прирост</th>
                    <th>Продолжительность<br></br>снижения</th>
                </tr>
            </table>
        </div>
    )
}

export default Main_DataTable