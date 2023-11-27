import Axios from "axios";
import { call, put, takeEvery } from "redux-saga/effects";
import api_address from "./apiAddress";
import Action from "../../types/Action";
import ACTIONS from "../actionCreators/ACTIONS";
import mainPageAC from "../actionCreators/mainPageAC";

async function getAllData(index_name: string, start_date: string, end_date: string, reduction: string, prefix: string, tolerance: string) {
    return await Axios.get(api_address + `/api/calculations/get_all_calculations?index_name=${index_name}&prefix=${prefix}&start_date=${start_date}&end_date=${end_date}&reduction=${reduction}&tolerance=${tolerance}`
    ).then((response) => {
        if (response.status === 200) {
            return response.data
        } else {
            if (response.status === 400) return "error";
        }
    })
    .catch((err) => {
        alert(err);
    });
}


function* getMainTable(action: Action) {
    const data = yield call(getAllData, action.index_name, action.start_date, action.end_date, action.reduction, action.prefix, action.tolerance)
    yield put(mainPageAC.setAllData(data));
}

function* watchGetAllData() {
    yield takeEvery(ACTIONS.GET_ALL_DATA, getMainTable);
}

export default watchGetAllData;