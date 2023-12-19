import Axios from "axios";
import { call, put, takeEvery } from "redux-saga/effects";
import api_address from "./apiAddress";
import Action from "../../types/Action";
import ACTIONS from "../actionCreators/ACTIONS";
import mainPageAC from "../actionCreators/mainPageAC";

async function getExcelData(index_name: string, start_date: string, end_date: string, reduction: string, prefix: string, tolerance: string) {
    return await Axios({
        url: api_address + `/api/calculations/get_excel_with_all_calculations?index_name=${index_name}&prefix=${prefix}&start_date=${start_date}&end_date=${end_date}&reduction=${reduction}&tolerance=${tolerance}`,
        method: 'GET',
        responseType: 'blob'
    }).then((response) => {
        const href = URL.createObjectURL(response.data)
        const link = document.createElement('a')
        link.href = href
        link.setAttribute('download', `${index_name}.xlsx`)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        URL.revokeObjectURL(href)
    })
    .catch((err) => {
        alert(err)
    })
}


function* getExcel(action: Action) {
    const data = yield call(getExcelData, action.index_name, action.start_date, action.end_date, action.reduction, action.prefix, action.tolerance)
    console.log(data)
}

function* watchGetExcelData() {
    yield takeEvery(ACTIONS.GET_EXCEL_DATA, getExcel);
}

export default watchGetExcelData;