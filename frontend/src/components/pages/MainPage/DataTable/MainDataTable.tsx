import React from "react";
import "./../../../../styles/MainDataTable.model.scss";


type Props = {
    data: any[];
    onLoad: boolean;
}

const MainDataTable = (props: Props) => {
    return (
        <div className="Main_DataTable">
            <table id="dataTable"  className="dataTable">
                <caption>Сформированные данные</caption>
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
                {props.data ? props.data.map((row) => (
                    <tr>
                        <th>{row[0]}</th>
                        <th>{row[2]}</th>
                        <th>{row[1]}</th>
                        <th>{row[4]}</th>
                        <th>{row[3]}</th>
                        <th>{row[5].toFixed(2)}</th>
                        <th>{row[6].toFixed(2)}</th>
                        <th>{row[7]}</th>
                    </tr>
                )) : <></>}
            </table>
        </div>
    )
}

export default MainDataTable