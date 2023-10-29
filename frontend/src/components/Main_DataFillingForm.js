import React from "react";
import "./../styles/Main_DataFillingForm.model.scss";

function Main_DataFillingForm() {
    return (
        <div className="Main_DataFillingForm">
            <form id="dataOutputSettings" name="dataOutputSettings" className="dataFillingForm">
                <div>
                    <label htmlFor="indexCode">Код индекса</label>
                </div>
                <div>
                    <input id="indexCode" name="indexCode" type="text" className="form-inpute-value"></input>
                </div>
                <div>
                    <label htmlFor="startDate">С</label>
                    <input id="startDate" name="startDate" type="date" className="form-input-date"></input>
                </div>
                <div>
                    <label htmlFor="endDate" className="form-label">По</label>
                    <input id="endDate" name="endDate" type="date" className="form-input-date"></input>
                </div>
                <div>
                    <label htmlFor="percentage">Процент для рассчета<br></br>снижения</label>
                </div>
                <div>
                    <input id="percentage" name="percentage" type="text" className="form-inpute-value"></input>
                </div>
                <div>
                    <button id="calculate" name="сalculate" className="form-button-accept">Рассчитать</button>
                </div>
            </form>
        </div>
    )
}

export default Main_DataFillingForm