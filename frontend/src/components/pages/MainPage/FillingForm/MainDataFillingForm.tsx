import React from "react";
import "./../../../../styles/MainDataFillingForm.model.scss";
import { Link } from "react-router-dom";


type Props = {
    getData: (
        index_name: string,
        start_date: string,
        end_date: string,
        reduction: string,
        tolerance?: string,
        prefix?: string
    ) => void;
    getExcelData: (
        index_name: string,
        start_date: string,
        end_date: string,
        reduction: string,
        tolerance?: string,
        prefix?: string
    ) => void;
}

function MainDataFillingForm(props: Props) {
    return (
        <div className="Main_DataFillingForm">
            <form id="dataOutputSettings" name="dataOutputSettings" className="dataFillingForm" onSubmit={(e) => {e.preventDefault();
                    props.getData((document.getElementById("indexCode") as HTMLInputElement)!.value!,
                    (document.getElementById("startDate") as HTMLInputElement)!.value!,
                    (document.getElementById("endDate") as HTMLInputElement)!.value!,
                    (document.getElementById("percentage") as HTMLInputElement)!.value!)}}>
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
                    <div>
                        <button id="calculate" name="сalculate" className="form-button-accept">Рассчитать</button>
                    </div>
                    <div>
                        <button id="download" name="download" className="form-button-download" onClick={(e) => {e.preventDefault();
                        props.getExcelData((document.getElementById("indexCode") as HTMLInputElement)!.value!,
                        (document.getElementById("startDate") as HTMLInputElement)!.value!,
                        (document.getElementById("endDate") as HTMLInputElement)!.value!,
                        (document.getElementById("percentage") as HTMLInputElement)!.value!)}}>Скачать</button>
                        <Link to="/Charts" className="form-button-download">Посмотреть графики</Link>
                    </div>
                </div>
            </form>
        </div>
    )
}

export default MainDataFillingForm