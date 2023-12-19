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
                <thead>
                    <tr>
                        <th>Дата</th>
                        <th>Цена</th>
                        <th>Откр.</th>
                        <th>Макс.</th>
                        <th>Мин.</th>
                        <th>Интегральная<br></br>сумма</th>
                        <th>Процентный<br></br>прирост</th>
                        <th>Продолжительность<br></br>снижения</th>
                        <th>Прогнозируемый<br></br>процент</th>
                        <th>Прогнозируемая<br></br>интегральная<br></br>сумма</th>
                        <th>Прогнозируемая<br></br>цена</th>
                        <th>ошибка</th>
                    </tr>
                </thead>
                <tbody>
                    {props.data ? props.data.map((row) => (
                        <tr>
                            <th>{row[0]}</th> {/* Дата */}
                            <th>{row[2]}</th> {/* Цена */}
                            <th>{row[1]}</th> {/* Откр */}
                            <th>{row[4]}</th> {/* Макс */}
                            <th>{row[3]}</th> {/* Мин */}
                            <th>{row[5].toFixed(2)}</th> {/* Интегральная сумма */}
                            <th>{row[6].toFixed(2)}</th> {/* Процентный прирост */}
                            <th>{row[7]}</th> {/* Продолжительность снижения */}
                            <th>{row[8].toFixed(2)}</th> {/* Прогнозируемый процент */}
                            <th>{row[9].toFixed(2)}</th> {/* Прогнозируемая сумма */}
                            <th>{row[10].toFixed(2)}</th> {/* Прогнозируемая цена */}
                            <th>{row[11].toFixed(2)}</th> {/* Ошибка */}
                        </tr>
                    )) : <></>}
                </tbody>
            </table>
        </div>
    )
}

export default MainDataTable